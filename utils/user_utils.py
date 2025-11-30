from enum import Enum


class UserRole(Enum):
    ADMIN = 1
    OWNER = 2
    MANAGER = 3

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]


class PackageName(Enum):
    BASIC = 1
    STANDARD = 2
    PREMIUM = 3

    @classmethod
    def get_package(cls):
        return [(key.value, key.name) for key in cls]


class Discount(Enum):
    NONE = 1
    AMOUNT = 2
    PERCENTAGE = 3

    @classmethod
    def get_discount(cls):
        return [(key.value, key.name) for key in cls]


class OrderStatus(Enum):
    REGULAR = 1
    ADJUSTMENT_INCREMENT = 2
    ADJUSTMENT_DECREMENT = 3
    RETURN = 4
    DEMAGE = 5
    CONDITIONAL = 6

    @classmethod
    def order_status(cls):
        return [(key.value, key.name) for key in cls]


class PaymentType(Enum):
    CASH = 1
    CARD = 2
    WALLET = 3

    @classmethod
    def payment_type(cls):
        return [(key.value, key.name) for key in cls]


class OrderType(Enum):
    HOMEDELIVERY = 1
    PICKUP = 2
    PREORDER = 3
    RESERVED = 4
    PERCEL = 5

    @classmethod
    def order_type(cls):
        return [(key.value, key.name) for key in cls]


class DeviceType(Enum):
    DESKTOP = 1
    MOBILE = 2
    BOTH = 3

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]
