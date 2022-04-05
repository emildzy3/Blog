

from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings
from django.dispatch import receiver
from django.urls import reverse
from mptt.models import TreeForeignKey
from news.models import Category


class CustomAccountManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, full_name, password, **other_fields):
        if not email:
            raise ValueError('Введи почту')
        email = self.normalize_email(email)
        if not full_name:
            full_name = email.split('@')[0]
        user = self.model(
            email=email,
            full_name=full_name,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, full_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Sorry но is_staff = False')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Sorry но is_superuser = False')
        if other_fields.get('is_active') is not True:
            raise ValueError('Sorry но is_active = False')

        return self.create_user(email, full_name, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Адрес электронной почты', unique=True)
    full_name = models.CharField(
        max_length=250, verbose_name='ФИО', blank=True)
    photo = models.ImageField(
        upload_to='AuthorUser_photo/%Y/%m/%d/', verbose_name='Фото автора')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_author = models.BooleanField(
        default=False, verbose_name='Автор контента?')
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomAccountManager()

    def __str__(self):
        return self.full_name

    # Ссылка на посты
    def get_absolute_url(self):
        return reverse('author_news_list', kwargs={'pk': self.pk})

    # Ссылка на профиль для читателей
    def get_profile_url(self):
        return reverse('author_profile', kwargs={'pk': self.pk})

    class Meta:
        ordering = ["-pk"]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ProfileAuthor (models.Model):

    author = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = RichTextField(verbose_name='Об авторе')
    achivment = models.CharField(
        max_length=350, verbose_name='Достижения', blank=True)
    category = TreeForeignKey(
        'news.Category', on_delete=models.CASCADE, verbose_name='Любимая Категория',
        default=1)

    def __str__(self):
        return self.author.full_name

    class Meta:
        ordering = ["-pk"]
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
