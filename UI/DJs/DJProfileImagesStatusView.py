from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle

from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import DJImageManager
################################################################################

__all__ = ("DJProfileImagesStatusView",)

################################################################################        
class DJProfileImagesStatusView(FroggeView):

    def __init__(self, user: User, images: DJImageManager):

        super().__init__(user, images)

        button_list = [
            AddThumbnailButton(),
            RemoveThumbnailButton(),
            AddBannerButton(),
            RemoveBannerButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
            
        self.set_button_attributes()

################################################################################        
class AddThumbnailButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.style = (
            ButtonStyle.success
            if self.view.ctx.logo is None
            else ButtonStyle.primary
        )
        self.label = (
            "Add Logo"
            if self.view.ctx.logo is None
            else "Change Logo"
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_thumbnail(interaction)
        await self.view.edit_message_helper(interaction=interaction, embed=self.view.ctx.status())

################################################################################
class AddBannerButton(FroggeButton):
    
    def __init__(self) -> None:
        super().__init__(
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.style = (
            ButtonStyle.success
            if self.view.ctx.banner is None
            else ButtonStyle.primary
        )
        self.label = (
            "Add Banner"
            if self.view.ctx.banner is None
            else "Change Banner"
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_banner(interaction)
        await self.view.edit_message_helper(interaction=interaction, embed=self.view.ctx.status())

################################################################################
class RemoveThumbnailButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Logo",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.disabled = self.view.ctx.logo is None
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.remove_thumbnail(interaction)
        await self.view.edit_message_helper(interaction=interaction, embed=self.view.ctx.status())
        
################################################################################
class RemoveBannerButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Banner",
            disabled=False,
            row=1
        )
        
    def set_attributes(self) -> None:
        self.disabled = self.view.ctx.banner is None
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.remove_banner(interaction)
        await self.view.edit_message_helper(interaction=interaction, embed=self.view.ctx.status())
        
################################################################################
