from django.db import models
from django.db.models import CharField, Model
from django.contrib.auth.models import User
from django_mysql.models import ListTextField

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=True)
    is_full_name_displayed = models.BooleanField(default=True)
    favored = ListTextField(base_field=CharField(max_length=10, null=True), size = 5)
    disliked = ListTextField(base_field=CharField(max_length=10, null=True), size = 5)
