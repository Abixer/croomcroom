from django import forms
from django.core.exceptions import ValidationError

from preview.models import Email

class EmailForm(forms.ModelForm):
    email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control input-lg email', 'placeholder':'Enter Email Address'}))
    class Meta:
        model = Email
        fields = ['email']