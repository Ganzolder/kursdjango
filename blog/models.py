from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Статья')
    picture = models.ImageField(upload_to='catalog/', **NULLABLE, verbose_name='Превью')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')


    def __str__(self):
        return f'{self.title}. Просмотрено {self.views_count} раз'

    class Meta:
        verbose_name = 'блоговая запись'
        verbose_name_plural = 'блоговые записи'