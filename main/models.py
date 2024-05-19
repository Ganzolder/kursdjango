from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Recipient(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    email = models.EmailField(unique=True, verbose_name="Email")
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    # last_message_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего сообщения')
    # creator = models.ForeignKey(User, verbose_name="Создатель", help_text="Кто создатель", **NULLABLE, on_delete=models.SET_NULL)
    objects = models.Manager()

    def __str__(self):
        return f'{self.name} {self.email} ({self.description})'

    class Meta:
        verbose_name = 'Адресат'
        verbose_name_plural = 'Адресаты'


'''        permissions = [
            (
                'set_published',
                'Can publish product'
            ),
            (
                'change_description',
                'Can change description'
            ),
            (
                'change_category',
                'Can change category'
            )
        ]'''


class Post(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    #period =
    status = models.CharField(max_length=50, verbose_name='Статус', **NULLABLE)
    started_at = models.DateTimeField(verbose_name='Начало', **NULLABLE)
    # last_message_at = models.DateTimeField(verbose_name='Дата последнего сообщения')
    # creator = models.ForeignKey(User, verbose_name="Создатель", help_text="Кто создатель", **NULLABLE, on_delete=models.SET_NULL)
    objects = models.Manager()

    def __str__(self):
        return f'{self.name} {self.email} ({self.description})'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
