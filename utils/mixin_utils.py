import random
import string
import secrets

# When user will create device token will automatically create random 10 digit string
letters = string.ascii_lowercase
random_device_token = ''.join(random.choice(letters) for i in range(10))


# Generate random password when user will create from package create time.
def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    return password.upper()


def email_body(email, password):
    body = (f'Thank you for signing up for our system. We have received your data please signin below access.\n'
            f'Email: {email}\n'
            f'Password: {password}')
    return body
