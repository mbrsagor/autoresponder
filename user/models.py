import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from user.manager import UserManager
from utils.user_utils import UserRole, DeviceType
from utils.mixin_utils import random_device_token


class DomainEntity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        abstract = True


class User(AbstractUser, DomainEntity):
    username = None
    name = models.CharField(max_length=50)
    store_id = models.IntegerField(default=0, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=14, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    role = models.IntegerField(choices=UserRole.get_choices(), default=UserRole.MANAGER.value)
    access = models.IntegerField(choices=DeviceType.get_choices(), default=DeviceType.BOTH.value)
    device_token = models.CharField(max_length=200, blank=True, null=True, default=random_device_token)

    def __str__(self):
        return self.name

    @property
    def role_name(self):
        if self.role == 1:
            return "Admin"
        elif self.role == 2:
            return "Owner"
        return "Manager"

    # Method to Put a Random OTP in the CustomerUser table.
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items_for_otp = []
        for i in range(6):
            num = random.choice(number_list)
            code_items_for_otp.append(num)
        code_string = "".join(str(item)
                              for item in code_items_for_otp)
        # A six digit random number from the list will be saved in top field
        self.otp = code_string
        # print(f"OTP: {self.otp}")
        super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = UserManager()


class Store(DomainEntity):
    """
    This class is used to store the user.
    """
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=14, unique=True, default='')
    address = models.TextField(blank=True, null=True, default='')
    email = models.EmailField(max_length=150, unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to='storeLogo/%m/%d', blank=True, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='storeOwner')
    users = models.ManyToManyField(User, related_name='storeUsers', blank=True)

    def __str__(self):
        return self.owner.name

    @property
    def owner_name(self):
        return self.owner.name

    @property
    def user_role(self):
        if self.owner.role == 1:
            return "Admin"
        elif self.owner.role == 2:
            return "Owner"
        return "Manager"


class Customer(DomainEntity):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=120, unique=True, blank=True, null=True)
    avatar = models.CharField(max_length=250, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='myCustomer')

    def __str__(self):
        return self.name


class Supplier(DomainEntity):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    contact_person = models.CharField(max_length=150)
    address = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=120, unique=True, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='mySupplier')

    def __str__(self):
        return self.name


class Due(DomainEntity):
    due = models.FloatField(default=0.00)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='DueSupplier')

    def __str__(self):
        return str(self.due)


def create_due(sender, instance, created, **kwargs):
    if created:
        profile, created = Due.objects.get_or_create(supplier=instance)
        return profile


post_save.connect(create_due, sender=Supplier)
