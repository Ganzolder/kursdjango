# Generated by Django 5.0.6 on 2024-06-08 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_user_message_creator_alter_post_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='creator',
        ),
    ]
