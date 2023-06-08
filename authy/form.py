from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    birth_date = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                     required=False, initial=timezone.now)

    class Meta:
        model = Profile
        exclude = ('user', )
