from ._Enum import FroggeEnum
################################################################################
class ChannelPurpose(FroggeEnum):
    
    TempJobs = 1
    Venues = 2
    Profiles = 3
    LogStream = 4
    Welcome = 5
    BotNotify = 6
    GroupTraining = 7
    PermJobs = 8

################################################################################
    @property
    def proper_name(self) -> str:
        
        if self.value == 1:
            return "Temporary Jobs Channel"
        elif self.value == 2:
            return "Venue Profiles Channel"
        elif self.value == 3:
            return "Staff Profiles Channel"
        elif self.value == 4:
            return "Log Stream"
        elif self.value == 6:
            return "Bot Restart Notification Channels"
        elif self.value == 7:
            return "Group Training Channel"
        elif self.value == 8:
            return "Permanent Jobs Channel"
        
        return self.name + " Channel"
    
################################################################################   
