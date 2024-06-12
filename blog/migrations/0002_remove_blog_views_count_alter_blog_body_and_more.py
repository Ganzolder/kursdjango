# Generated by Django 4.2.2 on 2024-06-12 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='views_count',
        ),
        migrations.AlterField(
            model_name='blog',
            name='body',
            field=models.TextField(verbose_name='Статья'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Заголовок'),
        ),
    ]
