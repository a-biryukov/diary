from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django import forms

from users.models import User


class UserRegisterForm(UserCreationForm):
    nickname = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        "class": "text-field__input",
        "placeholder": "",
        "id": "nick"
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
            "autofocus": True,
            "class": "text-field__input",
            "placeholder": "",
            "id": "email"
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "text-field__input",
        "placeholder": "",
        "id": "password1"
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "text-field__input",
        "placeholder": "",
        "id": "password2",
        }))

    class Meta:
        model = User
        fields = ('nickname', 'email', 'password1', 'password1')


class UserUpdateForm(UserChangeForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = User
        fields = ('avatar', 'nickname', 'email',)


class PasswordRecoveryForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
            "autofocus": True,
            "class": "text-field__input",
            "placeholder": "",
            "id": "email"
        }))


class UserAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
            "autofocus": True,
            "class": "text-field__input",
            "id": "login",
            "placeholder": ""
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "text-field__input",
        "id": "password",
        "placeholder": ""
        }))

    class Meta:
        model = User
        fields = ("username", "password",)


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "text-field__input",
        "id": "oldpassword",
        "placeholder": ""
        }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "text-field__input",
        "id": "newpassword1",
        "placeholder": ""
        }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "text-field__input",
        "id": "newpassword2",
        "placeholder": ""
        }))
