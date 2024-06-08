from django.contrib import admin

from main.models import Recipient, Message, Post

# Register your models here.
'''
admin.site.register(Post)
admin.site.register(Message)
admin.site.register(Recipient)'''

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('message', 'name', 'start_at', 'status',)

@admin.register(Message)
class PostAdmin(admin.ModelAdmin):
    list_display = ('subject', 'text',)

@admin.register(Recipient)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'enabled',)