from django.contrib import admin
from .models import Project, Donation, Motivation, Awareness
# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    pass

class DonationAdmin(admin.ModelAdmin):
    pass

class MotivationAdmin(admin.ModelAdmin):
    pass

class AwarenessAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project,ProjectAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Motivation, MotivationAdmin)
admin.site.register(Awareness, AwarenessAdmin)