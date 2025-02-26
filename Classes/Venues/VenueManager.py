from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Dict, Optional

from discord import Interaction, User, Embed, ForumChannel

from Classes.Common import ObjectManager
from UI.Common import FroggeView, ConfirmCancelView
from Utilities import Utilities as U
from .Venue import Venue

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("VenueManager", )

################################################################################
class VenueManager(ObjectManager):

    def __init__(self, state: StaffPartyBot) -> None:

        super().__init__(state)

################################################################################
    async def load_all(self, payload: Dict[str, Any]) -> None:

        self._managed = [Venue(self, **v) for v in payload["venues"]]

################################################################################
    async def finalize_load(self) -> None:

        for venue in self._managed:
            await venue.finalize_load()

################################################################################
    @property
    def venues(self) -> List[Venue]:

        return sorted(self._managed, key=lambda x: x.name.lower())  # type: ignore

################################################################################
    @property
    async def post_channel(self) -> Optional[ForumChannel]:

        return await self.bot.channel_manager.venue_post_channel

################################################################################
    async def status(self) -> Embed:

        pass

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        pass

################################################################################
    async def add_item(self, interaction: Interaction) -> None:

        pass

################################################################################
    async def modify_item(self, interaction: Interaction) -> None:

        pass

################################################################################
    async def remove_item(self, interaction: Interaction) -> None:

        pass

################################################################################
    def get_venue(self, name: str) -> Optional[Venue]:

        return next((v for v in self._managed if v.name.lower() == name.lower()), None)

################################################################################
    async def import_venue(
        self, interaction: Interaction, name: str, admin_user: Optional[User]
    ) -> None:

        exists = self.get_venue(name)
        if exists:
            error = U.make_error(
                title="Venue Exists",
                message=f"The venue `{name}` already exists.",
                solution=f"Try a different name for the venue."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        final_line = f"Are you sure you want to import venue __`{name}`__?"
        prompt = U.make_embed(
            title="Confirm Venue Import",
            description=(
                "The following venue information will be imported from your "
                f"XIV Venues listing into this server, "
                f"so long as {'the provided' if admin_user else 'your'} "
                "Discord user is listed as a manager on the venue.\n\n"

                "* Manager List\n"
                "* Banner Image\n"
                "* Description\n"
                "* Location\n"
                "* Website\n"
                "* Discord\n"
                "* Hiring Status\n"
                "* SFW Status\n"
                "* Tags\n"
                "* Mare ID\n"
                "* Mare Password\n"
                "* Normal Operating Schedule\n"
                "*(Schedule overrides are not imported.)*\n"
                f"{U.draw_line(text=final_line, extra=-2)}\n"
                f"{final_line}"
            )
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        msg = await interaction.followup.send("Please wait...")

        user_to_get = admin_user or interaction.user
        results = [
            v for v in
            self.bot.xiv_client.get_venues_by_manager(user_to_get.id)
            if v.name.lower() == name.lower()
        ]

        await msg.delete()

        if len(results) == 0:
            error = U.make_error(
                title="Unable to Import Venue",
                message=(
                    "An error occurred while attempting to import the venue.\n\n"

                    f"Either there are no venues with {'that user' if admin_user else 'you'} "
                    f"listed as a manager on the XIV Venues API, **or** there is no venue "
                    f"that is managed by {'that user' if admin_user else 'you'} with has "
                    f"the name you provided."
                ),
                solution=(
                    f"If {'that user is' if admin_user else 'you are'} not listed as a "
                    f"manager for any venues on the XIV Venues API, you will need to "
                    f"contact them to have {'that person' if admin_user else 'yourself'} "
                    f"added as a manager.\n\n"

                    f"If {'that user is' if admin_user else 'you are'} are listed as "
                    f"a manager for a venue, but the venue was not found, please ensure "
                    f"that you have entered the name of the venue correctly."
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        if len(results) > 1:
            error = U.make_error(
                title="Unable to Import Venue",
                message=(
                    "More than one venue was found with the name you provided "
                    f"that falls under {'the given' if admin_user else 'your'} management."
                ),
                solution="Please contact the bot owner for assistance."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        venue = await Venue.new(self, results[0])
        self._managed.append(venue)

        await self.bot.log.venue_created(venue)

        await venue.post(interaction, await self.post_channel, True)
        await venue.menu(interaction)

################################################################################
    async def remove_venue(self, interaction: Interaction, venue_name: str) -> None:

        venue = self.get_venue(venue_name)
        if venue is None:
            error = U.make_error(
                title="Venue Doesn't Exist",
                message=f"The venue `{venue_name}` hasn't been created yet.",
                solution=f"Use the `/admin import_venue` command to create the venue."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        await venue.remove(interaction)

################################################################################
    @staticmethod
    async def authenticate(venue: Venue, user: User, interaction: Interaction) -> bool:

        if user not in await venue.managers:
            error = U.make_error(
                title="Unauthorized User",
                message="You are not authorized to perform this action.",
                solution="Please contact an administrator for assistance."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return False

        return True

################################################################################
    async def toggle_user_mute(self, interaction: Interaction, name: str, user: User) -> None:

        venue = self.get_venue(name)
        if venue is None:
            error = U.make_error(
                title="Venue Doesn't Exist",
                message=f"The venue `{name}` hasn't been created yet.",
                solution=f"Use the `/admin import_venue` command to create the venue."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        if not await self.authenticate(venue, interaction.user, interaction):
            return

        await venue.toggle_user_mute(interaction, user)

################################################################################
