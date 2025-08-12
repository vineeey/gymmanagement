from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('trainer', 'Trainer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"


class CustomerProfile(models.Model):
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('weight_gain', 'Weight Gain'),
        ('muscle_building', 'Muscle Building'),
        ('fitness', 'General Fitness'),
        ('strength', 'Strength Training'),
    ]

    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    age = models.IntegerField()
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    diseases = models.TextField(blank=True, help_text="Any medical conditions or diseases")
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    trainer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='assigned_customers', limit_choices_to={'user_type': 'trainer'})

    def __str__(self):
        return f"{self.user_profile.user.username} - Customer"

    @property
    def bmi(self):
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)


class DietPlan(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='diet_plans')
    trainer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'trainer'})
    title = models.CharField(max_length=200)
    description = models.TextField()
    breakfast = models.TextField()
    lunch = models.TextField()
    dinner = models.TextField()
    snacks = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diet Plan for {self.customer.user_profile.user.username}"
