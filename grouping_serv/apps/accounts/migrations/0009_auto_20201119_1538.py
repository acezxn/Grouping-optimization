# Generated by Django 3.0.7 on 2020-11-19 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20201103_0659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='allowed_join',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='passcode',
            field=models.CharField(default=[], max_length=200),
            preserve_default=False,
        ),
    ]
