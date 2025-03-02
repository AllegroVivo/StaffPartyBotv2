from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from discord import User, Interaction, ButtonStyle

from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import ProfileImages
################################################################################

__all__ = ("SetRemoveImageView",)

################################################################################
class SetRemoveImageView(FroggeView):

    def __init__(self, owner: User, images: ProfileImages, image_type: Literal["Thumbnail", "Main"]):
        
        super().__init__(owner, images)

        assert image_type in ("Thumbnail", "Main")
        self.image_type: str = image_type
        
        button_list = [
            SetImageButton(image_type),
            RemoveImageButton(image_type),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
            
        self.set_button_attributes()
        
################################################################################
class SetImageButton(FroggeButton):
    
    def __init__(self, image_type: Literal["Thumbnail", "Main"]):
        
        super().__init__(
            style=ButtonStyle.success,
            label=f"Set {image_type} Image",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.ctx.set_image(interaction, self.view.image_type)
        await self.view.edit_message_helper(
            interaction, embed=self.view.ctx.image_status(self.view.image_type)
        )
        
################################################################################
class RemoveImageButton(FroggeButton):
    
    def __init__(self, image_type: Literal["Thumbnail", "Main"]):
        
        super().__init__(
            style=ButtonStyle.danger,
            label=f"Remove {image_type} Image",
            disabled=False,
            row=0
        )
        
    def set_attributes(self) -> None:
        if self.view.image_type == "Thumbnail":
            self.disabled = self.view.ctx.thumbnail is None
        else:
            self.disabled = self.view.ctx.main_image is None
        
    async def callback(self, interaction: Interaction):
        await self.view.ctx.remove_image(interaction, self.view.image_type)
        await self.view.edit_message_helper(
            interaction, embed=self.view.ctx.image_status(self.view.image_type)
        )
        
################################################################################
