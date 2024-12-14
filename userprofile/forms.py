from django import forms
from django.contrib.auth.models import User
from .models import Profile, ShippingAddress

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  

class ProfilePartialForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address1', 'address2', 'city_province', 'district']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'address1': forms.TextInput(attrs={'placeholder': 'Address Line 1', 'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'placeholder': 'Address Line 2', 'class': 'form-control'}),
            'city_province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Province'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
        }

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address1', 'address2', 'city_province', 'district']
        widgets = {
            'address1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'address2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}),
            'city_province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Province'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
        }