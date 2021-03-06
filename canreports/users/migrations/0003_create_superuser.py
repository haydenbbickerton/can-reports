# Generated by Django 2.0.4 on 2018-04-27 07:38

from django.db import migrations
from canreports.users.models import User

def create_superuser(apps, schema_editor):
    superuser = User()
    superuser.is_active = True
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.username = 'admin'
    superuser.email = 'admin@admin.net'
    superuser.set_password('password123')
    superuser.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20171227_2246'),
    ]

    operations = [
    	migrations.RunPython(create_superuser)
    ]
