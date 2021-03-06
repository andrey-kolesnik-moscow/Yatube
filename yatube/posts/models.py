from django import template
from django.db import models
from django.contrib.auth import get_user_model

register = template.Library()

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, null=False,
                             verbose_name='Название группы')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Путь')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        related_name='posts',
        on_delete=models.SET_NULL,
        verbose_name='Группа',
        help_text='Выберите группу')

    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ('-pub_date', '-pk')
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария')
    created = models.DateTimeField(
        'Дата создания комментария',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ('-created', '-pk')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор поста'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscribers_and_authors'),
        ]
