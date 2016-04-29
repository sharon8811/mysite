from django import forms
from ckeditor.widgets import CKEditorWidget


class ContactForm(forms.Form):
    sender = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=CKEditorWidget(), required=True)
