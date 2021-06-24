from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bucket.models import BucketUser

# Register your models here.
class BucketUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'user_id', 'date_joined', 'last_login', 'is_admin')
    search_fields = ('email', 'username')
    readonly_fields = ('user_id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(BucketUser, BucketUserAdmin)
