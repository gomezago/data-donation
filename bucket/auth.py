from django.contrib.auth.backends import BaseBackend
from .models import BucketUser

class BucketAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user, **kwargs):
        find_user = BucketUser.objects.filter(user_id=user['id']) #Returns Queryset
        if len(find_user) == 0:
            print("User was not found. Saving...")
            new_user = BucketUser.objects.create_user(user['email'], user['username'], user['id'])
            return new_user
        return list(find_user).pop(0)

    def get_user(self, user_id):
        try:
            return BucketUser.objects.get(pk=user_id)
        except BucketUser.DoesNotExist:
            return None