from __future__ import annotations

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Enums import DataCenter, GameWorld
################################################################################

__all__ = ("DataCenterWorldSelectView",)

################################################################################
class DataCenterWorldSelectView(FroggeView):

    def __init__(self, user: User):
        
        super().__init__(user, None)
        
        self.add_item(DataCenterSelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class DataCenterSelect(Select):
    
    def __init__(self):
                                   
        super().__init__(
            placeholder="Select a data center...",
            options=DataCenter.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        dc = DataCenter(int(self.values[0]))
        
        self.placeholder = dc.proper_name
        self.disabled = True
        self.view.add_item(WorldSelect(dc))
        
        await interaction.edit(view=self.view)
    
################################################################################
class WorldSelect(Select):
    
    def __init__(self, dc: DataCenter):
                                   
        super().__init__(
            placeholder="Select a world...",
            options=GameWorld.select_options_by_dc(dc),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )
        
        self.dc = dc
        
    async def callback(self, interaction: Interaction):
        self.view.value = (self.dc, GameWorld(int(self.values[0])))
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore
    
################################################################################
