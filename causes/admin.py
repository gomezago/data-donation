from django.contrib import admin
from causes.models import Cause
from causes.models import Donation

# Register your models here.
class CauseAdmin(admin.ModelAdmin):
    pass

class DonationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cause,CauseAdmin)
admin.site.register(Donation, DonationAdmin)