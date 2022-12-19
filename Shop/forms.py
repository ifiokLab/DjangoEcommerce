
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *

class CustomerCreationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label
        self.fields['first_name'].widget.attrs['placeholder'] = self.fields['first_name'].label
        self.fields['last_name'].widget.attrs['placeholder'] = self.fields['last_name'].label
        self.fields['password1'].widget.attrs['placeholder'] = self.fields['password1'].label
        self.fields['password1'].widget.attrs['id'] = 'password1'
        self.fields['password2'].widget.attrs['placeholder'] = self.fields['password2'].label
        self.fields['password2'].widget.attrs['id'] = 'password2'


    class Meta:
        model = myuser
        fields= ('email', 'first_name', 'last_name', 'password1', 'password2')


    def save(self, commit=True):
        user= super().save(commit=True)
        user.is_customer = True
        user.is_active =True

        if commit:
            user.save()

        return user

class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': _(
            "Please enter the correct Email and password for a Customers"
            "account. Note that both fields are case-sensitive "

        ),
    }
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_customer:
            raise ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username':self.username_field.verbose_name}
            )

class SellerLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': _(
            "Please enter the correct Email and password for a Sellers"
            "account. Note that both fields are case-sensitive "

        ),
    }
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_seller:
            raise ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username':self.username_field.verbose_name}
            )

class SellerCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SellerCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label
        self.fields['first_name'].widget.attrs['placeholder'] = self.fields['first_name'].label
        self.fields['last_name'].widget.attrs['placeholder'] = self.fields['last_name'].label
        self.fields['password1'].widget.attrs['placeholder'] = self.fields['password1'].label
        self.fields['password1'].widget.attrs['id'] = 'password1'
        self.fields['password2'].widget.attrs['placeholder'] = self.fields['password2'].label
        self.fields['password2'].widget.attrs['id'] = 'password2'

    class Meta:
        model = myuser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        user.is_active =True
        if commit:
            user.save()

        return user


PAYMENT =(
    ('P', 'Paystack'),
    ('C', 'Crypto')
)

DeliveryMethod =(
    ('D', 'Door Delivery'),
    ('P', 'Pickup Station(Cheaper Shipping Fees than Door Delivery')
)

class CheckoutForm(forms.Form):
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT)
    delivery_method = forms.ChoiceField(widget=forms.RadioSelect, choices=DeliveryMethod)

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields= '__all__'

class SellerProfileForm(ModelForm):
    class Meta:
        model = Seller
        fields = '__all__'

class ConfirmForm(forms.Form):
    confirm = forms.BooleanField(label='Confirm', required=True)