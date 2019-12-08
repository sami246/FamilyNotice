from enum import Enum

class userType(Enum):
    FamilyMember = 'Regular Family Member'
    Gaurdian = "Gaurdian"


    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)
