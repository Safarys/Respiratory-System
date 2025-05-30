# Generated by Django 5.1.6 on 2025-04-07 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0006_prescription_doctor_id'),
        ('predict', '0017_rename_name_diagnostictest_patid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave_doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('reason', models.TextField()),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predict.user')),
            ],
        ),
    ]
