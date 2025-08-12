from django.contrib import admin
from .models import UserProfile, CustomerProfile, DietPlan

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'created_at']
    list_filter = ['user_type', 'created_at']

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'age', 'height', 'weight', 'goal', 'trainer']
    list_filter = ['goal', 'trainer']

@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ['customer', 'trainer', 'title', 'created_at']
    list_filter = ['created_at', 'trainer']
