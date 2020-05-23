from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from gst_field.modelfields import GSTField, PANField


class CongoUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('User must have a valid phone number')

        user = self.model(phone_number=phone_number, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CongoUser(AbstractBaseUser):
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CongoUserManager()

    def __str__(self):
        return str(self.phone_number)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class CongoUserProfile(models.Model):
    RETAILER = 'R'
    WHOLESALER = 'W'
    BUSINESS_TYPE_CHOICES = [
        (RETAILER, 'Retailer'),
        (WHOLESALER, 'Wholesaler'),
    ]

    ELECTRONICS = 'EC'
    APPLIANCES = 'AP'
    FASHION = 'FS'
    HOME_DECOR = 'HD'
    GROCERY = 'GC'
    OTHERS = 'OT'
    BUSINESS_CATEGORIES = [
        (ELECTRONICS, 'Electronics'),
        (APPLIANCES, 'Appliances'),
        (FASHION, 'Fashion'),
        (HOME_DECOR, 'Home Decoration'),
        (GROCERY, 'Groceries'),
        (OTHERS, 'Others')
    ]

    congo_user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_verified = models.BooleanField(default=False)
    business_name = models.CharField(max_length=50)
    gst_number = GSTField()
    business_type = models.CharField(
        max_length=1, choices=BUSINESS_TYPE_CHOICES, default=RETAILER)
    business_category = models.CharField(
        max_length=2, choices=BUSINESS_CATEGORIES)

    def __str__(self):
        return '{} - {} {}'.format(self.business_name, self.first_name, self.last_name)
