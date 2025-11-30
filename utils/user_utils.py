from enum import Enum


class UserRole(Enum):
    ADMIN = 1
    EMPLOYEE = 2

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]


class Gender(Enum):
    MAIL = 1
    FEMALE = 2
    OTHER = 3

    @classmethod
    def get_gender(cls):
        return [(key.value, key.name) for key in cls]
