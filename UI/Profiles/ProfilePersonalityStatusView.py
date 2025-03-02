from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import Interaction, User, ButtonStyle

from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import ProfilePersonality
################################################################################

__all__ = ("ProfilePersonalityStatusView",)

################################################################################        
class ProfilePersonalityStatusView(FroggeView):

    def __init__(self, user: User, personality: ProfilePersonality):

        super().__init__(user, personality)

        button_list = [
            LikesButton(),
            DislikesButton(),
            PersonalityButton(),
            AboutMeButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################        
class LikesButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Likes",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.likes)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_likes(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class DislikesButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Dislikes",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.dislikes)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_dislikes(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class PersonalityButton(FroggeButton):
    
    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Personality",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.personality)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_personality(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class AboutMeButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="About Me/Bio",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.about_me)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_aboutme(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
