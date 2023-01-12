from django.contrib import admin
from atm.models import DataSlipDonation
# Register your models here.

class DataSlipAdmin(admin.ModelAdmin):
    pass

admin.site.register(DataSlipDonation, DataSlipAdmin)