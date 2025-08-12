from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerSignupForm, TrainerSignupForm, CustomerProfileForm, DietPlanForm
from .models import UserProfile, CustomerProfile, DietPlan


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('email')
            user.save()

            UserProfile.objects.create(
                user=user,
                user_type='customer',
                phone=form.cleaned_data.get('phone')
            )

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please complete your profile.')
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('accounts:customer_profile')
    else:
        form = CustomerSignupForm()
    return render(request, 'accounts/customer_signup.html', {'form': form})


def trainer_signup(request):
    if request.method == 'POST':
        form = TrainerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('email')
            user.save()

            UserProfile.objects.create(
                user=user,
                user_type='trainer',
                phone=form.cleaned_data.get('phone')
            )

            username = form.cleaned_data.get('username')
            messages.success(request, f'Trainer account created for {username}!')
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('dashboard:home')
    else:
        form = TrainerSignupForm()
    return render(request, 'accounts/trainer_signup.html', {'form': form})


@login_required
def customer_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user, user_type='customer')

    try:
        customer_profile = user_profile.customerprofile
    except CustomerProfile.DoesNotExist:
        customer_profile = None

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_profile = user_profile
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard:home')
    else:
        form = CustomerProfileForm(instance=customer_profile)

    return render(request, 'accounts/customer_profile.html', {'form': form})


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

