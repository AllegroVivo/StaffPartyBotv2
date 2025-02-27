from __future__ import annotations

from discord import Interaction, User
from discord.ui import Select

from Enums import Hours, Minutes
from UI.Common import FroggeView, CloseMessageButton
################################################################################

__all__ = ("TimeSelectView",)

################################################################################
class TimeSelectView(FroggeView):

    def __init__(self, user: User, incl_unavailable: bool = True):
        
        super().__init__(user, None)

        self.add_item(HourSelect(incl_unavailable))
        self.add_item(CloseMessageButton())
    
################################################################################
class HourSelect(Select):
    
    def __init__(self, incl_unavailable: bool):
        
        super().__init__(
            placeholder="Select the hour...",
            options=(
                Hours.select_options()
                if incl_unavailable
                else Hours.limited_select_options()
            ),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        hour = Hours(int(self.values[0]))
        if hour == Hours.Unavailable:  # Unavailable
            self.view.value = hour
            self.view.complete = True
            await interaction.edit()
            await self.view.stop()  # type: ignore
            return

        self.placeholder = hour.proper_name
        self.disabled = True
            
        self.view.add_item(MinuteSelect(hour))
        await interaction.edit(view=self.view)
    
################################################################################
class MinuteSelect(Select):

    def __init__(self, hour: Hours):

        super().__init__(
            placeholder="Select the minutes...",
            options=Minutes.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )
        
        self.hour: Hours = hour

    async def callback(self, interaction: Interaction):
        minutes = int(Minutes(int(self.values[0])).proper_name[3:])

        self.view.value = self.hour.value, minutes
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore

################################################################################
