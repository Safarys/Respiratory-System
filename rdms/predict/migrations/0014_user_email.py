# Generated by Django 5.1.6 on 2025-03-22 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0013_remove_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
