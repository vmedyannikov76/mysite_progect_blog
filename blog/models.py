from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# создадим конкретно прикладной менеждер для вытягивания только опубликованных постов
class PublishedMeneger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликовано'

    title = models.CharField('Заголовок поста',
                             max_length=250)
    slug = models.SlugField('Короткая метка',
                            unique_for_date='publish',
                            max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts',
                               verbose_name='Автор')
    body = models.TextField('Содержание поста')
    publish = models.DateTimeField('дата публикации', default=timezone.now)
    created = models.DateTimeField('дата создания', auto_now_add=True)
    updated = models.DateTimeField('дата обновления', auto_now=True)
    status = models.CharField('Статус', max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()  # менеджер применяемый по умолчанию
    published = PublishedMeneger()  # конкретно прикладной менеджер

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])
