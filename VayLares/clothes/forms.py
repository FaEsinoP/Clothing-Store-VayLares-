from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *


class AddGoodForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Не выбрано'

    class Meta:
        model = Clothes
        fields = ['title', 'slug', 'content', 'photo', 'alternative_photo', 'price', 'gender', 'is_published', 'brand',
                  'category', 'subcategory']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повтор пароля')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


VARIANTS = [(i, str(i)) for i in range(1, 21)]


class UserProfileForm(UserChangeForm):
    fields = ['first_name', 'last_name', 'image', 'username', 'gender', 'email']

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'gender', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'text-field__input'}),
            'last_name': forms.TextInput(attrs={'class': 'text-field__input'}),
            'username': forms.TextInput(attrs={'class': 'text-field__input'}),
            'gender': forms.Select(attrs={'class': 'gender-select'}),
            'email': forms.TextInput(attrs={'class': 'text-field__input'}),
        }

    def clean_first_name(self):
        if self.cleaned_data['first_name'] == 0:
            raise ValidationError("Пустой first_name")
        return self.cleaned_data['first_name']