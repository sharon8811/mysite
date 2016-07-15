from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'age', 'height', 'nickname', 'first_name', 'last_name', 'email')
        widgets = {
            'age': forms.DateInput(attrs={'class': 'datepicker'}),
        }

