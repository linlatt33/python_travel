from django.contrib import admin
from .models import Topic, Places, Message, User


# Register your models here.


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('upload_by', 'topic', 'name', 'located', 'hotel_name', 'description')


class RegisterAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'order_hotel')


class AdminUser(admin.ModelAdmin):
    list_display = ('name', 'email', 'bio')


admin.site.register(Topic)
admin.site.register(Places, PlaceAdmin)
admin.site.register(Message, RegisterAdmin)
admin.site.register(User, AdminUser)
