from django.contrib import admin

from main.models import Recipient, Message, Post, PostLogs


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('message', 'name', 'start_at', 'next_send_date', 'status', 'period')


@admin.register(Message)
class PostAdmin(admin.ModelAdmin):
    list_display = ('subject', 'text',)


@admin.register(Recipient)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'enabled',)


@admin.register(PostLogs)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'try_date', 'result', 'user', 'error_message')
