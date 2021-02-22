from django.contrib import admin
from causes.models import Cause

# Register your models here.
class CauseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cause,CauseAdmin)