from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class BucketUserManager(BaseUserManager):

    def create_user(self, email, username, user_id, password=None):
        print("Inside Bucket User Manager")
        if not email:
            raise ValueError("Email address is required.")

        if not username:
            raise ValueError("Username is required.")

        if not user_id:
            raise ValueError("User ID is required.")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            user_id = user_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, user_id, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            user_id = user_id,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class BucketUser(AbstractBaseUser):
    email               = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username            = models.CharField(max_length=30, unique=True)
    user_id             = models.CharField(max_length=60, unique=True, default=None)
    date_joined         = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name="last login", auto_now=True)

    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)

    hide_email          = models.BooleanField(default=True)

    objects = BucketUserManager()

    USERNAME_FIELD = 'email' # Field to log in with
    REQUIRED_FIELDS = ['username', 'user_id'] # Required fields


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

