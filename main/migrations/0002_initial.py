# Generated by Django 5.0.6 on 2024-06-04 13:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='создатель'),
        ),
        migrations.AddField(
            model_name='post',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.message', verbose_name='Сообщение'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='создатель'),
        ),
        migrations.AddField(
            model_name='postlogs',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.post', verbose_name='Рассылка'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='creator',
            field=models.ForeignKey(blank=True, help_text='Создал', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
        migrations.AddField(
            model_name='post',
            name='recipient',
            field=models.ManyToManyField(to='main.recipient', verbose_name='Получатель'),
        ),
        migrations.AddField(
            model_name='result',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.post', verbose_name='Рассылка'),
        ),
        migrations.AddField(
            model_name='result',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='создатель'),
        ),
        migrations.AddField(
            model_name='postlogs',
            name='result',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.result', verbose_name='Результат попытки'),
        ),
    ]
