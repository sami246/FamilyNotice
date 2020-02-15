from enum import Enum

class userType(Enum):
    FamilyMember = 'Regular Family Member'
    Guardian = "Guardian"


    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)

class genderType(Enum):
    Male = 'Male'
    Female = "Female"
    Other = 'Prefer not to say'


    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)

class DaysMeals(Enum):
    MonB = 'Monday Breakfast'
    TueB = 'Tuesday Breakfast'
    WedB = 'Wednesday Breakfast'
    ThurB = 'Thursday Breakfast'
    FriB = 'Friday Breakfast'
    SatB = 'Saturday Breakfast'
    SunB = 'Sunday Breakfast'
    MonL = 'Monday Lunch'
    TueL = 'Tuesday Lunch'
    WedL = 'Wednesday Lunch'
    ThurL = 'Thursday Lunch'
    FriL = 'Friday Lunch'
    SatL = 'Saturday Lunch'
    SunL = 'Sunday Lunch'
    MonD = 'Monday Dinner'
    TueD = 'Tuesday Dinner'
    WedD = 'Wednesday Dinner'
    ThurD = 'Thursday Dinner'
    FriD = 'Friday Dinner'
    SatD = 'Saturday Dinner'
    SunD = 'Sunday Dinner'


    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)

class MealChoice(Enum):
    Breakfast = 'Breakfast'
    Lunch = 'Lunch'
    Dinner = 'Dinner'



    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)
