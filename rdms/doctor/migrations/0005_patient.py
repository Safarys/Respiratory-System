# Generated by Django 5.1.6 on 2025-03-24 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_prescription'),
        ('predict', '0017_rename_name_diagnostictest_patid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('address', models.TextField(max_length=100)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predict.user')),
            ],
        ),
    ]
