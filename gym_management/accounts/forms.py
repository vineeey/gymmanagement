from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, CustomerProfile, DietPlan


class CustomerSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class TrainerSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    verification_code = forms.CharField(max_length=50, help_text="Enter trainer verification code")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'verification_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code')
        if code != 'trainer@skpm':
            raise forms.ValidationError("Invalid trainer verification code.")
        return code


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['age', 'height', 'weight', 'diseases', 'goal']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'diseases': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'goal': forms.Select(attrs={'class': 'form-control'}),
        }


class DietPlanForm(forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = ['title', 'description', 'breakfast', 'lunch', 'dinner', 'snacks', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'breakfast': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'lunch': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'dinner': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'snacks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
