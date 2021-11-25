from django import forms
from .models import *
from django.contrib.auth import get_user_model


non_allowed_usernames = ['abc']

user = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = user.objects.filter(username__iexact=username)

        if username in non_allowed_usernames:
            raise forms.ValidationError("This is an invalid username, please pick another.")
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = user.objects.filter(email__iexact=email)

        if qs.exists():
            raise forms.ValidationError("This is email is already in use.")
        
        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = user.objects.filter(username__iexact=username)

        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        
        return username


class ProductForm(forms.ModelForm):
  
    class Meta:
        model = Product
        fields = [
            'brand', 
            'model', 
            'description', 
            'size', 
            'price', 
            'image'
        ]


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = [
            'name',
            'last_name',
            'address',
        ]


class DemandForm(forms.ModelForm):

    class Meta:
        model = Demand
        fields = [
            'date',
            'payment_confirmed'
        ]


class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = [
            'amount'
        ]


class DeliveryForm(forms.ModelForm):

    class Meta:
        model = Delivery
        fields = [
            'district',
            'city'
        ]


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = [
            'number',
            'valid_date',
            'holders_name',
            'cvv',
        ]

