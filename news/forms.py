from django import forms
from .models import Article


class SubmitArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('name', 'writer', 'short_text', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'writer': forms.TextInput(attrs={'class': 'form-control'}),
            'short_text': forms.Textarea(attrs={'class': 'form-control', 'cols': 80, 'rows': 5}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'cols': 80, 'rows': 13}),
            }
