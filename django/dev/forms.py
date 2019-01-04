from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from .models import Message

class LoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True,
          'placeholder': 'username'}),
    )
    password = forms.CharField(
        label= ("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}),
    )


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content']
        widgets = {'content': forms.Textarea()}