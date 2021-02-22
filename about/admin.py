from django.contrib import admin
from about.models import Post, Category

# Register your models here.
class PostAdmin(admin.ModelAdmin): #Empty admin classes. Can be customized to choose what to show on admin page
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin) #Register the models with the admin classes.
admin.site.register(Category, CategoryAdmin)