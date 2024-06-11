from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=35,
                             verbose_name="Телефон",
                             blank=True, null=True,
                             help_text="Введите номер телефона")
    enabled = models.BooleanField(default=True, verbose_name='Активен')

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

        permissions = [
            (
                'change_activity',
                'Can block user'
            ),
            (
                'view_users',
                'Can view list of users'
            ),
            (
                'view_recipients',
                'Can view list of recipients'
            ),
            (
                'view_posts',
                'Can view list of posts'
            )
        ]

    def __str__(self):
        return self.email
