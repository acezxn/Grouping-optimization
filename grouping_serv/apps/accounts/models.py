from django.db import models
from django.db.models import CharField, Model
from django.contrib.auth.models import User
from django_mysql.models import ListTextField
import json

# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", null=True
    )
    is_full_name_displayed = models.BooleanField(default=True)
    # classrooms = ListTextField(base_field=CharField(max_length=10, null=True), size=5)

    favored = ListTextField(base_field=CharField(max_length=10, null=True), size=5)
    disliked = ListTextField(base_field=CharField(max_length=10, null=True), size=5)

    # favored = models.CharField(max_length=200)
    # disliked = models.CharField(max_length=200)

    def set_relation(self, x, y):
        self.favored = json.dumps(x)
        self.disliked = json.dumps(y)

    @classmethod
    def create(cls, id):
        obj = cls(user_id=id)
        obj.set_relation([], [])
        return obj
