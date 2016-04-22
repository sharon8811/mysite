from django import forms
from django.forms import ModelForm
from .models import Question
from django.utils import timezone


class QuestionAjaxForm(ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'pub_date')
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control'}),
            'pub_date': forms.DateInput(attrs={'class': 'form-control', 'default': timezone.now()}),
            }
