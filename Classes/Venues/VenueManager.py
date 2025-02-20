from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Dict, Optional

from discord import Interaction, User, Embed, ForumChannel

from Classes.Common import ObjectManager, LazyChannel
from UI.Common import FroggeView, ConfirmCancelView
from .Venue import Venue
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("VenueManager", )

################################################################################
class VenueManager(ObjectManager):

    __slots__ = (
        "_post_channel",
    )

################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        super().__init__(state)

        self._post_channel: LazyChannel = LazyChannel(self, None)

################################################################################
    async def load_all(self, payload: Dict[str, Any]) -> None:

        self._managed = [Venue(self, *v) for v in payload["venues"]]
        self._post_channel = LazyChannel(self, payload["post_channel_id"])

################################################################################
    @property
    def venues(self) -> List[Venue]:

        return sorted(self._managed, key=lambda x: x.name.lower())  # type: ignore

################################################################################
    @property
    async def post_channel(self) -> Optional[ForumChannel]:

        return await self._post_channel.get()

    @post_channel.setter
    def post_channel(self, value: Optional[ForumChannel]) -> None:

        self._post_channel.set(value)

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
    async def import_venue(self, interaction: Interaction, name: str) -> None:

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
                "XIV Venues listing into this server, so long as your Discord "
                "user is listed as a manager for the venue.\n\n"

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

        results = [
            v for v in
            await self.bot.xiv_client.get_venues_by_manager(interaction.user.id)
            if v.name.lower() == name.lower()
        ]

        await msg.delete()

        if len(results) == 0:
            error = U.make_error(
                title="Unable to Import Venue",
                message=(
                    "An error occurred while attempting to import the venue.\n\n"

                    "Either there are no venues with you listed as a manager on "
                    "the XIV Venues API, **or** there is no venue that you manage "
                    "that has the name you provided."
                ),
                solution=(
                    "If you are not listed as a manager for any venues on the XIV "
                    "Venues API, you will need to contact them to have yourself "
                    "added as a manager.\n\n"

                    "If you are listed as a manager for a venue, but the venue "
                    "was not found, please ensure that you have entered the name "
                    "of the venue correctly."
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        if len(results) > 1:
            error = U.make_error(
                title="Unable to Import Venue",
                message=(
                    "More than one venue was found with the name you provided "
                    "that falls under your management."
                ),
                solution="Please contact the bot owner for assistance."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        xiv_venue = results[0]
        venue = await Venue.new(self, xiv_venue, interaction)
        self._managed.append(venue)

        await self.bot.log.venue_created(venue)

        await venue.post(interaction, self.post_channel, True)
        await venue.menu(interaction)

################################################################################
