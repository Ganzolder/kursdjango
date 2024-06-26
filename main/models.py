from django.db import models
from django.conf import settings
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Recipient(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    email = models.EmailField(unique=True, verbose_name="Email")
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    creator = models.ForeignKey(User, verbose_name="Создатель", help_text="Создал", on_delete=models.SET_NULL,
                                **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    enabled = models.BooleanField(default=True, verbose_name='Активен')
    # last_message_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего сообщения')
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


class Message(models.Model):
    subject = models.CharField(max_length=250, verbose_name='Тема письма')
    text = models.TextField(verbose_name='Сообщение')
    creator = models.ForeignKey(User, verbose_name='создатель', on_delete=models.SET_NULL, **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    enabled = models.BooleanField(default=True, verbose_name='Активен')
    objects = models.Manager()

    def __str__(self):
        return f'{self.subject} {self.creator}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Post(models.Model):

    PERIOD_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('created', 'Создано и готово к рассылке'),
        ('published', 'В рассылке'),
        ('canceled', 'Отменено'),
    ]

    recipient = models.ManyToManyField(Recipient, verbose_name='Получатель')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Создатель', on_delete=models.CASCADE, **NULLABLE)
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.SET_NULL, **NULLABLE)
    name = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    start_at = models.DateTimeField(verbose_name='Начало рассылки', **NULLABLE)
    period = models.CharField(max_length=50, verbose_name='Периодичность', choices=PERIOD_CHOICES)
    status = models.CharField(max_length=50, verbose_name='Статус', default='draft', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    enabled = models.BooleanField(default=True, verbose_name='Активен')
    next_send_date = models.DateTimeField(verbose_name='Дата следующей отправки', null=True, blank=True)
    last_send_status = models.CharField(max_length=50, verbose_name='Статус последней отправки', null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.name} ({self.description})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    permissions = [
        (
            'set_published',
            'Can publish posts'
        )
    ]


class PostLogs(models.Model):
    post = models.ForeignKey(Post, verbose_name='Рассылка', on_delete=models.SET_NULL, **NULLABLE)
    try_date = models.DateTimeField(verbose_name='Дата попытки')
    result = models.CharField(max_length=50, verbose_name='Результат попытки', **NULLABLE, choices=[('success', 'Успех'), ('failed', 'Ошибка')])
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.SET_NULL, **NULLABLE)
    error_message = models.TextField(null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.post} -> ({self.try_date})'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
