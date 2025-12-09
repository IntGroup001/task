from enum import Enum


class FuelTypeEnum(Enum):
    petrol = "petrol"
    diesel = "diesel"
    electric = "electric"
    hybrid = "hybrid"
    lpg = "lpg"


class UserRoleEnum(Enum):
    admin = "admin"
    car_specialist = "car_specialist"
    user = "user"
