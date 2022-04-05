

from django.shortcuts import render
from .forms import CustomReaderCreationForm, AuthorizationUserForm, CustomAuthorCreationForm, AdvancedUpdateForm, BaseUpdateForm, CustomPasswordResetForm
from .models import ProfileAuthor
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from .backends import AuthBackend
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .utils import send_email_verify, send_email_for_author_application
from django.contrib.auth.tokens import default_token_generator as token_generator
from users.forms import UserCreationForm, AuthenticationForm, ApplicationForRegistrationAuthorForm
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import get_template
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


def get_author_profile(request, pk):
    actual_author = User.objects.get(pk=pk)
    if request.user == actual_author:
        return render(request, 'users/profile.html')
    return render(request, 'users/author_profile.html',
                           {'actual_author': actual_author})


def get_profile(request):
    return render(request, 'users/profile.html')


def write_data_profile(form_with_basic_data, form_with_advanced_data=None):
    if form_with_advanced_data is not None:
        email = form_with_basic_data.cleaned_data['email']
        full_name = form_with_basic_data.cleaned_data['full_name']
        bio = form_with_advanced_data.cleaned_data['bio']
        achivment = form_with_advanced_data.cleaned_data['achivment']
        category = form_with_advanced_data.cleaned_data['category']
        photo = form_with_basic_data.cleaned_data['photo']
        form_with_basic_data.save()
        form_with_advanced_data.save()
    else:
        email = form_with_basic_data.cleaned_data['email']
        full_name = form_with_basic_data.cleaned_data['full_name']
        photo = form_with_basic_data.cleaned_data['photo']
        new_profile = form_with_basic_data.save()


def edit_author_profile(request):
    try:
        profile_author = ProfileAuthor.objects.get(author=request.user.id)
    except ObjectDoesNotExist:
        ProfileAuthor.objects.create(author=request.user)
        profile_author = ProfileAuthor.objects.get(author=request.user.id)
    if request.method == "POST":
        form_with_basic_data = BaseUpdateForm(
            request.POST, request.FILES, instance=request.user)
        form_with_advanced_data = AdvancedUpdateForm(
            request.POST, instance=profile_author)
        if form_with_basic_data.is_valid() and form_with_advanced_data.is_valid():
            write_data_profile(form_with_basic_data,
                               form_with_advanced_data)
            messages.success(request, 'Профиль успешно изменен')
            return redirect(reverse('profile'))
        else:
            messages.warning(request, 'Ошибка валидации')
    else:
        form_with_basic_data = BaseUpdateForm(instance=request.user)
        form_with_advanced_data = AdvancedUpdateForm(instance=profile_author)
    return render(request, 'users/profile_update.html',
                  {'form_with_basic_data': form_with_basic_data,
                   'form_with_advanced_data': form_with_advanced_data})


def edit_reader_profile(request):
    if request.method == "POST":
        form_with_basic_data = BaseUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form_with_basic_data.is_valid():
            write_data_profile(form_with_basic_data)
            messages.success(request, 'Профиль успешно изменен')
            return redirect(reverse('profile'))
        else:
            messages.warning(request, 'Ошибка валидации')
    else:
        form_with_basic_data = BaseUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html',
                  {'form_with_basic_data': form_with_basic_data})


def profile_update(request):
    if request.user.is_author:
        return edit_author_profile(request)
    else:
        return edit_reader_profile(request)


def sending_email_confirmation(request):
    return render(request, 'users/confirm_email.html')


def activate_reader(request, uidb64, token):
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            reader = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            reader = None
        return reader

    reader = get_user(uidb64)

    if reader is not None and token_generator.check_token(reader, token):
        reader.is_active = True
        reader.save()
        login(request, reader, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, f'Привет, {reader.full_name}')
        return redirect('home')
    return redirect('user_is_not_found')


def user_is_not_found(request):
    return render(request, 'users/user_is_not_found.html')


class PasswordResetViewCustom(PasswordResetView):
    template_name = 'users/reset_password.html'
    subject_template_name = 'users/recovery_email_subject.txt'
    email_template_name = 'users/reset_password_email.html'
    form_class = CustomPasswordResetForm


class PasswordResetDoneViewCustom (PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirmViewCustom (PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'


class PasswordResetCompleteViewCustom(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


def registration_reader(request):
    if request.method == 'POST':
        form = CustomReaderCreationForm(request.POST)
        if form.is_valid():
            reader = User.objects.create_user(
                email=form.cleaned_data['email'],
                full_name=form.cleaned_data['full_name'],
                password=form.cleaned_data.get('password1'),

            )
            send_email_verify(request, reader)
            return redirect('confirm_email')
    else:
        form = CustomReaderCreationForm()

    return render(request, 'users/registration.html', {'form': form})


@permission_required('users.add_newuser', raise_exception=True)
def registration_for_author(request):
    if request.method == 'POST':
        form = CustomAuthorCreationForm(request.POST, request.FILES)
        if form.is_valid():
            author = User.objects.create_user(
                email=form.cleaned_data['email'],
                full_name=form.cleaned_data['full_name'],
                password=form.cleaned_data.get('password1'),
                photo=form.cleaned_data['photo'],
            )
            author.is_author = True
            group_author = Group.objects.get(name='Автор')
            author.groups.add(group_author)
            author.save()
            messages.success(request, 'Автор зарегестрирован')
            return redirect('registration_for_author')
        else:
            messages.warning(request, 'Ошибка валидации')
    else:
        form = CustomAuthorCreationForm()
    return render(request, 'users/registration_for_author.html', {'form': form})


def apply_for_registration(request):
    if request.method == 'POST':
        form = ApplicationForRegistrationAuthorForm(
            request.POST, request.FILES)
        if form.is_valid():

            context = {
                'full_name_author': form.cleaned_data['full_name_author'],
                'email': form.cleaned_data['email'],
                'photo': request.FILES['photo'],
                'example_article': form.cleaned_data['example_article'],
                'about': form.cleaned_data['about'],
                'achievement': form.cleaned_data['achievement'],
                'article_category': form.cleaned_data['article_category'],
            }

            try:
                send_email_for_author_application(request, context)
                messages.success(request, 'Заявка отправленна ')
                return redirect('apply_for_registration')

            except:
                messages.warning(
                    request, 'Не удалось отправить сообщение')
                return redirect('apply_for_registration')

        else:
            messages.warning(request, 'Валидация не пройдена')
            return redirect('apply_for_registration')

    else:
        form = ApplicationForRegistrationAuthorForm()
    return render(request, 'users/apply_for_registration.html', {'form': form})


def authorizationUser(request):
    if request.method == 'POST':
        form = AuthorizationUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Привет, {user.full_name}')
                    return redirect('home')
                else:
                    send_email_verify(request, user)
                    messages.warning(
                        request, 'Аккаунт деактивирован. На указанаю при\
                        регистрации почту была отправленна ссылка с повторной\
                        активацией')
                    return redirect('authorization')
            else:
                messages.warning(request, 'Пользователь не найден. Проверте\
                                           введенные данные ')
                return redirect('authorization')
        else:
            messages.warning(request, 'Введен некоректный email')
            return redirect('authorization')

    else:
        form = AuthorizationUserForm()
    return render(request, 'users/authorizationUser.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('authorization')
