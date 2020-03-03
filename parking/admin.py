from django.contrib import admin
from parking.models import *


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'phone', 'email']


class CarAdmin(admin.ModelAdmin):
    list_display = ['pk', 'car_num', 'ticket_num', 'ticket_limit', 'user']


class LogAdmin(admin.ModelAdmin):
    list_display = ['pk', 'car_number', 'car_in', 'car_out', 'user_stat', 'pay_val', 'car_stat']


admin.site.register(User, UserAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Log, LogAdmin)
