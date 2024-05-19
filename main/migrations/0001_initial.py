# Generated by Django 5.0.6 on 2024-05-15 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Адресат',
                'verbose_name_plural': 'Адресаты',
            },
        ),
    ]
