# Generated by Django 4.2.7 on 2024-02-07 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_email_verified',
            field=models.BooleanField(default=False),
        ),
    ]
