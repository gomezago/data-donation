from django.contrib import admin
from .models import Project, Donation
# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    pass

class DonationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project,ProjectAdmin)
admin.site.register(Donation, DonationAdmin)