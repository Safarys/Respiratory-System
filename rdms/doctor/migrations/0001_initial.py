# Generated by Django 5.1.6 on 2025-03-22 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField()),
                ('Specialization', models.CharField(max_length=40)),
                ('medical_li_no', models.CharField(max_length=40)),
                ('qualification', models.CharField(max_length=40)),
            ],
        ),
    ]
