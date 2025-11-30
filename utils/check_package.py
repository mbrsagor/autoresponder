def category_package(package_type, categories):
    if package_type == 1 and not len(categories) < 20:
        return False
    elif package_type == 2 and not len(categories) < 50:
        return False
    else:
        return True


def brand_package(package_type, brands):
    if package_type == 1 and not len(brands) < 20:
        return False
    elif package_type == 2 and not len(brands) < 50:
        return False
    return True


def check_products(package_type, products):
    if package_type == 1 and not len(products) < 150:
        return False
    elif package_type == 2 and not len(products) < 300:
        return False
    return True


def check_suppliers(package_type, suppliers):
    if package_type == 1 and not len(suppliers) < 20:
        return False
    elif package_type == 2 and not len(suppliers) < 30:
        return False
    return True


def check_customers(package_type, customers):
    if package_type == 1 and not len(customers) < 100:
        return False
    elif package_type == 2 and not len(customers) < 20:
        return False
    return True


def check_coupons(package_type, coupons):
    if package_type == 1 and not len(coupons) < 10:
        return False
    elif package_type == 2 and not len(coupons) < 20:
        return False
    else:
        return True


def check_accounts(package_type, accounts):
    if package_type == 1 and not len(accounts) < 2:
        return False
    elif package_type == 2 and not len(accounts) < 5:
        return False
    return True


def check_users(package_type, users):
    if package_type == 1 and not len(users) < 5:
        return False
    elif package_type == 2 and not len(users) < 10:
        return False
    else:
        return True
