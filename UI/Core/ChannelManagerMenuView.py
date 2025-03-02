from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle, User

from Enums import ChannelPurpose
from UI.Common import CloseMessageButton, FroggeButton, FroggeView

if TYPE_CHECKING:
    from Classes import ChannelManager
################################################################################

__all__ = ("ChannelManagerMenuView",)

################################################################################
class ChannelManagerMenuView(FroggeView):

    def __init__(self, owner: User, mgr: ChannelManager):
        
        super().__init__(owner, mgr)
        
        button_list = [
            UpdateChannelButton(ChannelPurpose.Welcome, 0),
            UpdateChannelButton(ChannelPurpose.LogStream, 0),
            UpdateChannelButton(ChannelPurpose.Profiles, 0),
            UpdateChannelButton(ChannelPurpose.Venues, 0),
            UpdateChannelButton(ChannelPurpose.GroupTraining, 1),
            UpdateChannelButton(ChannelPurpose.TempJobs, 1),
            UpdateChannelButton(ChannelPurpose.BotNotify, 1),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()
        
################################################################################
class UpdateChannelButton(FroggeButton):
    
    def __init__(self, purpose: ChannelPurpose, row: int):
        
        super().__init__(
            style=ButtonStyle.primary,
            label=purpose.proper_name.rstrip("Channel"),
            disabled=False,
            row=row
        )

        self.purpose: ChannelPurpose = purpose

    def set_attributes(self) -> None:
        channel = self.view.ctx.get_channel(self.purpose)
        if isinstance(channel, list):
            if len(channel) == 0:
                channel_id = None
            else:
                channel_id = channel[0].id
        else:
            channel_id = channel.id

        self.set_style(channel_id)

    async def callback(self, interaction):
        await self.view.ctx.set_channel(interaction, self.purpose)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
