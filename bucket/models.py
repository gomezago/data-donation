from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from utils.bucket_functions import create_thing, new_thing

# Create your models here.
class BucketUserManager(BaseUserManager):

    def create_user(self, email, username, user_id, token, password=None):
        print("Inside Bucket User Manager")
        if not email:
            raise ValueError("Email address is required.")

        if not username:
            raise ValueError("Username is required.")

        if not user_id:
            raise ValueError("User ID is required.")

        if not token:
            raise ValueError("Token is required.")


        thing = create_thing(new_thing('DDD Thing', 'Thing to Manage Donations', 'DDD Data'), token)
        if thing.ok:
            thingId = thing.json()['id']
        else:
            raise ValueError("Something went wrong.")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            user_id = user_id,
            thing_id= thingId
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, user_id, password):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            user_id = user_id,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)
        return user

class BucketUser(AbstractBaseUser):
    email               = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username            = models.CharField(max_length=30, unique=True)
    user_id             = models.CharField(max_length=60, unique=True, default=None, primary_key=True)
    date_joined         = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name="last login", auto_now=True)
    thing_id            = models.CharField(max_length=200, unique=True, default=None, null=True)

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

class OAuth2Token(models.Model):
    token_type      = models.CharField(max_length=40)
    access_token    = models.CharField(max_length=200)
    refresh_token   = models.CharField(max_length=200)
    expires_at      = models.PositiveIntegerField()
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def to_token(self):
        return dict(
            access_token = self.access_token,
            token_type = self.token_type,
            refresh_token = self.refresh_token,
            expires_at = self.expires_at,
        )