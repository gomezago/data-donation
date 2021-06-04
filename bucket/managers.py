from django.contrib.auth import models

class BucketUserManager (models.UserManager):
    def create_new_bucket_user(self, user):
        print("Into Bucket User Manager")
        new_user = self.create(
            id=user["id"],
            email=user["email"],
            email_verified=user["email_verified"],
            name=user["name"],
            username=user["given_name"],
            sid=user["sid"],
            # last_login done by Django
        )
        return new_user