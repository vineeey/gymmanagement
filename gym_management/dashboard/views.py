from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.models import UserProfile, CustomerProfile, DietPlan
from accounts.forms import DietPlanForm


@login_required
def dashboard_home(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.user_type == 'customer':
        try:
            customer_profile = user_profile.customerprofile
            diet_plans = DietPlan.objects.filter(customer=customer_profile).order_by('-created_at')
        except CustomerProfile.DoesNotExist:
            return redirect('accounts:customer_profile')

        context = {
            'user_profile': user_profile,
            'customer_profile': customer_profile,
            'diet_plans': diet_plans
        }
        return render(request, 'dashboard/customer_dashboard.html', context)

    else:  # trainer
        customers = CustomerProfile.objects.filter(trainer=user_profile)
        all_customers = CustomerProfile.objects.all()
        context = {
            'user_profile': user_profile,
            'customers': customers,
            'all_customers': all_customers
        }
        return render(request, 'dashboard/trainer_dashboard.html', context)


@login_required
def create_diet_plan(request, customer_id):
    trainer_profile = get_object_or_404(UserProfile, user=request.user, user_type='trainer')
    customer_profile = get_object_or_404(CustomerProfile, id=customer_id)

    if request.method == 'POST':
        form = DietPlanForm(request.POST)
        if form.is_valid():
            diet_plan = form.save(commit=False)
            diet_plan.customer = customer_profile
            diet_plan.trainer = trainer_profile
            diet_plan.save()
            messages.success(request, 'Diet plan created successfully!')
            return redirect('dashboard:customer_detail', customer_id=customer_id)
    else:
        form = DietPlanForm()

    context = {
        'form': form,
        'customer': customer_profile
    }
    return render(request, 'dashboard/create_diet_plan.html', context)


@login_required
def customer_detail(request, customer_id):
    trainer_profile = get_object_or_404(UserProfile, user=request.user, user_type='trainer')
    customer_profile = get_object_or_404(CustomerProfile, id=customer_id)
    diet_plans = DietPlan.objects.filter(customer=customer_profile).order_by('-created_at')

    context = {
        'customer': customer_profile,
        'diet_plans': diet_plans
    }
    return render(request, 'dashboard/customer_detail.html', context)


@login_required
def assign_trainer(request, customer_id):
    if request.user.userprofile.user_type != 'trainer':
        messages.error(request, 'Only trainers can assign themselves to customers.')
        return redirect('dashboard:home')

    trainer_profile = get_object_or_404(UserProfile, user=request.user, user_type='trainer')
    customer_profile = get_object_or_404(CustomerProfile, id=customer_id)

    customer_profile.trainer = trainer_profile
    customer_profile.save()
    messages.success(request, f'You are now assigned to {customer_profile.user_profile.user.username}!')
    return redirect('dashboard:customer_detail', customer_id=customer_id)
