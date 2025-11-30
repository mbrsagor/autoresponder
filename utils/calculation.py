def discount_calculation(price, discount):
    try:
        result = (price * discount) / 100
        return result
    except ZeroDivisionError:
        return None


_price = 100
_discount = 20

final = discount_calculation(_price, _discount)
