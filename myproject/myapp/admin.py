from django.contrib import admin

from myapp import models
# Register your models here.

class MembersAdmin(admin.ModelAdmin):
    list_display = ('reg_number','reg_type','tickets','date','event')

class EventAdmin(admin.ModelAdmin):
    list_display = ('name','address','date')

admin.site.register(models.Members,MembersAdmin)
admin.site.register(models.Event,EventAdmin)