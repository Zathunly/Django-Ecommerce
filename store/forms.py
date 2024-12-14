from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from decimal import Decimal
from .models import Product, Category, SubCategory
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminSelectWidget

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

class RegisterForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = None

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = None

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = None

class ProductForm(forms.ModelForm):
    price = forms.CharField(
        widget=UnfoldAdminTextInputWidget(attrs={
            'placeholder': 'Enter price as text'
        })
    )

    # Fields from CategoryForm
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=UnfoldAdminSelectWidget(attrs={
            'id': 'id_category',
            'class': 'custom-category-select'
        }),
        label="Category"
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.none(),
        widget=UnfoldAdminSelectWidget(attrs={
            'id': 'id_subcategory',
            'class': 'custom-subcategory-select'
        }),
        label="Subcategory"
    )

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Handle price and sale_price initial values
        if 'price' in self.initial and self.initial['price'] is not None:
            price_value = Decimal(self.initial['price']).normalize()
            price_str = format(price_value, 'f')
            if price_str.endswith('.0'):
                price_str = price_str[:-2]
            self.initial['price'] = price_str

        if 'sale_price' in self.initial and self.initial['sale_price'] is not None:
            sale_price_value = Decimal(self.initial['sale_price']).normalize()
            sale_price_str = format(sale_price_value, 'f')
            if sale_price_str.endswith('.0'):
                sale_price_str = sale_price_str[:-2]
            self.initial['sale_price'] = sale_price_str

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = SubCategory.objects.none()
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=self.instance.category)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price:
            normalized_price = price.replace('.', '').replace(',', '.')
            try:
                cleaned_price = Decimal(normalized_price)
                return cleaned_price.normalize()
            except Decimal.InvalidOperation:
                raise forms.ValidationError("Price must be a valid number.")
        return price

    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price', None)
        if sale_price:
            normalized_sale_price = sale_price.replace('.', '').replace(',', '.')
            try:
                cleaned_sale_price = Decimal(normalized_sale_price)
                return cleaned_sale_price.normalize()
            except Decimal.InvalidOperation:
                raise forms.ValidationError("Sale price must be a valid number.")
        return None