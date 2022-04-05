

from django import forms
from django.forms.widgets import Textarea
from captcha.fields import CaptchaField
from .models import Post, Comment
from django.forms import ModelForm
from mptt.forms import TreeNodeChoiceField


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'preview_photo', 'category',
                  'is_published')


class FeedbackForm (forms.Form):
    message = forms.CharField(widget=forms.Textarea, label="Сообщение")
    captcha = CaptchaField(label='Введите текст с картинки')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text', 'parent')
