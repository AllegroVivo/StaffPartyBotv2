from ._Enum import FroggeEnum
################################################################################
class RoleType(FroggeEnum):

    StaffMain = 1
    StaffNotValidated = 2
    VenueManagement = 3
    Trainee = 4
    TraineeHiatus = 5

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 1:
            return "Staff Main Role"
        elif self.value == 2:
            return "Staff Pending Role"
        elif self.value == 3:
            return "Venue Management Role"
        elif self.value == 4:
            return "Trainee Main Role"
        elif self.value == 5:
            return "Trainee Hiatus Role"

        return self.name
    
################################################################################
    