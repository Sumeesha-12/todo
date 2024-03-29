
from django import forms
from remainder.models import Todos
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from remainder.models import Todos

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        



class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todos
        fields=["name"]
