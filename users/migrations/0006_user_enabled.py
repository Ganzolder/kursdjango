# Generated by Django 4.2.2 on 2024-06-11 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
    ]
