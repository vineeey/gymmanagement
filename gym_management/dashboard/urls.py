from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('create-diet-plan/<int:customer_id>/', views.create_diet_plan, name='create_diet_plan'),
    path('assign-trainer/<int:customer_id>/', views.assign_trainer, name='assign_trainer'),
]
