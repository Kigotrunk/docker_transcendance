from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from myaccount.models import Account


class FormRegistration(UserCreationForm):

    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address !")

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is link whith an existant account.")
    
    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            account = Account.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"username {username} already use ")

class FormAuthentification(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("invalid login")

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'hide_email', 'profile_picture']




