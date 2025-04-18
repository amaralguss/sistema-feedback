from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Feedback


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['nota', 'comentario', 'anonimo']
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'placeholder': 'Deixe um comentário (opcional)'}),
        }
