from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
    
class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, password=None, username=None):
        if not email:
            raise ValueError("User must have an email address")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not phone_number:
            raise ValueError("User must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, phone_number, password, username=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    username = models.CharField(max_length=50, unique=True, verbose_name="Username")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email Address")
    phone_number = models.CharField(max_length=11, verbose_name="Phone Number")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date Joined")
    last_login = models.DateTimeField(auto_now=True, verbose_name="Last Login")
    is_admin = models.BooleanField(default=False, verbose_name="Is Admin")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    is_staff = models.BooleanField(default=False, verbose_name="Is Staff")
    is_superadmin = models.BooleanField(default=False, verbose_name="Is Super Admin")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    
    objects = AccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True