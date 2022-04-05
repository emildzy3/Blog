

from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordResetForm
from .models import ProfileAuthor
from django import forms
from django.contrib.auth.forms import AuthenticationForm, _unicode_ci_compare
from news.models import Category
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth import get_user_model


User = get_user_model()




# Редактирование профиля автора:
# 1. Базовая Информация - BaseUpdateForm
# 2. Дополнитльная информация - AdvancedUpdateForm

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        email_field_name = User.get_email_field_name()
        active_users = User._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

class BaseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'photo']


class AdvancedUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfileAuthor
        fields = ['bio', 'achivment', 'category']


class CustomAuthorCreationForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('email', 'full_name', 'photo', 'password1', 'password2')


class CustomReaderCreationForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('email', 'full_name', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class AuthorizationUserForm(forms.Form):
    username = forms.EmailField(label='Почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class ApplicationForRegistrationAuthorForm(forms.Form):
    full_name_author = forms.CharField(max_length=100, strip=True, label='ФИО')
    email = forms.EmailField(label='Почта')
    photo = forms.ImageField(label='Ваша фотография')
    article_category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                              label='Категория вашей статьи')
    example_article = forms.CharField(widget=CKEditorWidget(),
                                      label='Пример статьи')
    about = forms.CharField(max_length=100, widget=forms.Textarea, strip=True,
                            label='Информация о Вас', required=False)
    achievement = forms.CharField(
        max_length=100, widget=forms.Textarea, strip=True, label='Достижения',
        required=False)
