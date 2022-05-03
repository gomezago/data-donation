from django.contrib import admin
from .models import Project, Donation, Motivation, Awareness, InitialAwareness, FinalAwareness, DeletedPoint, DeleteDonation, City
# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    pass

class DonationAdmin(admin.ModelAdmin):
    pass

class MotivationAdmin(admin.ModelAdmin):
    pass

class AwarenessAdmin(admin.ModelAdmin):
    pass

class InitialAwarenessAdmin(admin.ModelAdmin):
    pass

class FinalAwarenessAdmin(admin.ModelAdmin):
    pass

class DeletedPointAdmin(admin.ModelAdmin):
    pass

class DeleteDonationAdmin(admin.ModelAdmin):
    pass

class CityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project,ProjectAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Motivation, MotivationAdmin)
admin.site.register(Awareness, AwarenessAdmin)
admin.site.register(InitialAwareness, InitialAwarenessAdmin)
admin.site.register(FinalAwareness, FinalAwarenessAdmin)
admin.site.register(DeletedPoint, DeletedPointAdmin)
admin.site.register(DeleteDonation, DeleteDonationAdmin)
admin.site.register(City, CityAdmin)