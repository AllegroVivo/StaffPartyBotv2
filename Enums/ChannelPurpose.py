from ._Enum import FroggeEnum
################################################################################
class ChannelPurpose(FroggeEnum):
    
    TempJobs = 1
    Venues = 2
    Profiles = 3
    LogStream = 4
    Welcome = 5
    Internship = 6
    PermJobs = 7
    DJProfiles = 8
    SpecialEvents = 9
    Services = 10
    Communication = 11

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
            return "Internship Channel"
        elif self.value == 7:
            return "Permanent Jobs Channel"
        elif self.value == 8:
            return "DJ Profiles Channel"
        elif self.value == 9:
            return "Special Events Channel"
        
        return self.name + " Channel"
    
################################################################################   
