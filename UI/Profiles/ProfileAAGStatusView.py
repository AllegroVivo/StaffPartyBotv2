from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle

from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import ProfileAtAGlance
################################################################################

__all__ = ("ProfileAAGStatusView",)

################################################################################        
class ProfileAAGStatusView(FroggeView):

    def __init__(self, user: User, aag: ProfileAtAGlance):

        super().__init__(user, aag)

        button_list = [
            SetAccentColorButton(),
            SetRPJobsButton(),
            SetCustomURLButton(),
            SetRaceClanButton(),
            SetGenderPronounButton(),
            SetMareButton(),
            SetOrientationButton(),
            SetHeightButton(),
            SetAgeButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class SetAccentColorButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Accent Color",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx._color)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_color(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class SetRPJobsButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="RP Jobs",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.jobs)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_jobs(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class SetCustomURLButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Custom URL",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.url)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_url(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class SetGenderPronounButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Gender/Pronouns",
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.gender)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_gender(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class SetRaceClanButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Race/Clan",
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.race)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_raceclan(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class SetOrientationButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Orientation",
            disabled=False,
            row=2
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.orientation)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_orientation(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class SetHeightButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Height",
            disabled=False,
            row=2
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.height)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_height(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class SetAgeButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Age",
            disabled=False,
            row=2
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.age)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_age(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class SetMareButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Mare ID",
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.mare)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_mare(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
