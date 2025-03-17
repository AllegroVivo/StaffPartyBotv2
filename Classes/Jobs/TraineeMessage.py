from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Dict, List

from discord import Embed, EmbedField, Interaction, ChannelType, Message, NotFound

from Classes.Common import LazyMessage
from Enums import Position
from UI.Jobs import TraineeMessagePickupView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import StaffPartyBot, Profile
################################################################################

__all__ = ("TraineeMessage", )

################################################################################
class TraineeMessage:

    __slots__ = (
        "_state",
        "_post_msg",
    )

################################################################################
    def __init__(self, state: StaffPartyBot, post_url: Optional[str] = None) -> None:

        self._state: StaffPartyBot = state
        self._post_msg: LazyMessage = LazyMessage(self, post_url)

################################################################################
    def load(self, payload: Dict[str, Any]) -> None:

        self._post_msg = LazyMessage(self, payload["post_url"])

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._state

################################################################################
    @property
    async def post_message(self) -> Optional[Message]:

        return await self._post_msg.get()

    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:

        self._post_msg.set(value)

    @property
    def post_url(self) -> Optional[str]:

        return self._post_msg.url

################################################################################
    def update(self) -> None:

        self.bot.db.update.top_level(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "trainee_message_url": self._post_msg.url
        }

################################################################################
    async def status(self) -> Embed:

        return U.make_embed(
            title="__TRAINER/TRAINEE MATCHING__",
            description=(
                "This is the sign up message for the trainer/trainee matching system. "
                "If you are a trainer and wish to pick up a trainee, please select the "
                "trainee's name from the selector below.\n\n"

                "Please consider your selection carefully. Once you have selected a "
                "trainee, you will be unable to change your selection without consulting "
                "a member of management.\n"
                f"{U.draw_line(extra=49)}"
            ),
            fields=await self.available_trainee_fields(),
        )

################################################################################
    async def available_trainee_fields(self) -> List[EmbedField]:

        position_dict: Dict[Position, List[Profile]] = { p: [] for p in Position }

        for profile in self.bot.profile_manager.profiles_wanting_training():
            if len(profile.availability) >= 1:
                for pos in profile.desired_trainings:
                    position_dict[pos].append(profile)

        fields = []
        for pos, profiles in position_dict.items():
            value = ""
            if len(profiles) == 0:
                value = "`No trainees available.`\n"
            else:
                for p in profiles:
                    dc = (
                        "" if not p.data_centers
                        else f" - *({'/'.join([region.abbreviation for region in p.data_centers])})*"
                    )
                    value += (
                        f"[{p.char_name}]({p.post_url}){dc} - {(await p.user).mention}\n"
                    )

            fields.append(EmbedField(name=pos.proper_name, value=value, inline=False))

        return fields

################################################################################
    async def post(self, interaction: Interaction) -> None:

        if await self.update_post_components():
            return

        channel = await U.select_channel(
            interaction=interaction,
            bot=self.bot,
            channel_type="Trainee Message",
            restrictions=[ChannelType.text]
        )
        if channel is None:
            return

        view = TraineeMessagePickupView(self)
        self.bot.add_view(view)

        self.post_message = await channel.send(embed=await self.status(), view=view)
        await interaction.respond("Signup message posted.", ephemeral=True)

################################################################################
    async def update_post_components(self, update_embed: bool = True, update_view: bool = True) -> bool:

        post_message = await self.post_message
        if post_message is None:
            return False

        try:
            if update_embed and not update_view:
                await post_message.edit(embed=await self.status())
                return True

            view = TraineeMessagePickupView(self)
            self.bot.add_view(view, message_id=post_message.id)

            if update_view and not update_embed:
                await post_message.edit(view=view)
            else:
                await post_message.edit(embed=await self.status(), view=view)
        except NotFound:
            self.post_message = None
            return False
        else:
            return True

################################################################################
