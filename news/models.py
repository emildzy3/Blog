

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.urls import reverse, reverse_lazy



class Post (models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = RichTextUploadingField(verbose_name='Текст новости')
    preview_photo = models.ImageField(
        upload_to='preview_photo/%Y/%m/%d/', verbose_name='Обложка',
        blank=True)
    date_creation = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    date_change = models.DateTimeField(
        auto_now=True, verbose_name='Дата изменения')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='Автор')
    category = TreeForeignKey(
        'Category', on_delete=models.CASCADE, verbose_name='Категория')
    is_published = models.BooleanField(verbose_name='Опубликовать?',
                                       default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('full_news', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('post_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'pk': self.pk})

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Category(MPTTModel):
    title = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_news_list', args=[str(self.pk)])


class Comment(MPTTModel):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='Автор коментраия')
    comment_text = models.TextField(verbose_name='Текст коментария')
    publication_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class MPTTMeta:
        order_insertion_by = ['publication_date']

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.comment_text
