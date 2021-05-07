from django.contrib import admin
from .models import BhavData
# Register your models here.

@admin.register(BhavData)
class AdminBhavData(admin.ModelAdmin):
    list_display = ['id','code','name','open','high','low','close','date']