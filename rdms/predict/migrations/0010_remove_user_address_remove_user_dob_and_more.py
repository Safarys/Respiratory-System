# Generated by Django 5.1.6 on 2025-03-22 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0009_delete_appointment_delete_doctor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]
