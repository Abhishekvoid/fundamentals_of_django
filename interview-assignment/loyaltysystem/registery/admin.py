from django.contrib import admin
from .models import AppUser, MenuItem, Order, VisitCount

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display=['phone_number', 'username']
    search_fields = ['phone_number', 'username']
    

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available']
    list_filter = ['available']
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'timestamp']
    list_filter = ['timestamp']
    raw_id_fields = ['user']  # Dropdown → ID search

@admin.register(VisitCount)
class VisitCountAdmin(admin.ModelAdmin):
    list_display = ['user', 'visits']
    raw_id_fields = ['user']
