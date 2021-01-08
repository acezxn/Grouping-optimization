from django import forms
from django_mysql.models import ListTextField
from django.db import models
from django.db.models import CharField, Model


class NameForm(forms.Form):
    favored = forms.CharField(max_length=10)
    disliked = forms.CharField(max_length=10)
    # favored = forms.ListTextField(base_field=CharField(max_length=10, null=True), size = 5)
    # disliked = forms.ListTextField(base_field=CharField(max_length=10, null=True), size = 5)
    # def __str__(self):
    #     return ' '.join([
    #
    #         favored,
    #         disliked,
    #
    #
    #     ])
class SignupForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
