from django.contrib.auth.backends import BaseBackend
from .models import BucketUser

class BucketAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user) -> BucketUser:
        #Check if user exists in db
        find_user = BucketUser.objects.filter(id=user["id"])
        if len(find_user) == 0:
            print("User was not found... Saving User")
            #Save the user
            new_user = BucketUser.objects.create_new_bucket_user(user)
            print(new_user)
            return new_user
        return find_user