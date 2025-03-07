from ._Enum import FroggeEnum
################################################################################
class Month(FroggeEnum):

    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12
    
################################################################################
    def days(self) -> int:

        if self in (Month.February,):
            return 29

        if self in (Month.April, Month.June, Month.September, Month.November):
            return 30

        return 31

################################################################################
