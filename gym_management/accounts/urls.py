from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    # Replace the auth_views.LogoutView line with:
    path('logout/', views.logout_view, name='logout'),

    path('customer-signup/', views.customer_signup, name='customer_signup'),
    path('trainer-signup/', views.trainer_signup, name='trainer_signup'),
    path('customer-profile/', views.customer_profile, name='customer_profile'),
]
