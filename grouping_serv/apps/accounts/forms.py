from django import forms
from django_mysql.models import ListTextField
from django.db import models
from django.db.models import CharField, Model
from captcha.fields import CaptchaField
from django.utils.safestring import mark_safe


class NameForm(forms.Form):
    captcha = CaptchaField(label=mark_safe("Captcha:"))
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
