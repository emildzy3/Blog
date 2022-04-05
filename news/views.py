

from django.shortcuts import render
from .models import Post, Category, Comment
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.shortcuts import redirect
from .forms import FeedbackForm, AddPostForm, CommentForm
from django.contrib import messages
from users.models import ProfileAuthor
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from .utils import send_feedback_email
from django.db.models import Q



# Для уменьшения количества повторяющегося кода
def get_pagination(request, query):
    paginator = Paginator(query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # ЗАмена list_all_news
    page_numbers = paginator.get_elided_page_range()
    pg = {
        'page_obj': page_obj,
        'paginator': paginator,
        'page_numbers': page_numbers,
        'page_number': page_number,
    }
    return pg


def author_full_list(request):

    # Не работает:
    # authors = NewUser.objects.annotate(num=Count('post')).filter(is_author=True, num__gt=0).select_related('profileauthor__category','profileauthor__bio')

    return render(request, 'news/author_full_list.html')


def post_delete(request, pk):
    actual_post = Post.objects.get(pk=pk)
    actual_user = request.user
    if actual_user == actual_post.author:
        if request.method == 'POST':
            actual_post.delete()
            messages.success(request, 'Пост удален')
            return redirect('home')
        return render(request, 'news/post_delete.html', {'post': actual_post})

    else:
        messages.warning(request, 'Вы можете удалять только свои посты')
        return redirect(actual_post)


def post_update(request, pk):
    actual_post = Post.objects.get(pk=pk)
    actual_user = request.user
    if actual_user == actual_post.author:
        if request.method == "POST":
            form = AddPostForm(request.POST, request.FILES,
                               instance=actual_post)
            if form.is_valid():
                update_actual_post = form.save()
                messages.success(request, 'Пост изменен')
                return redirect(update_actual_post)
            else:
                messages.success(request, 'Ошибка валидации')
                return redirect('post_update')
        else:
            form = AddPostForm(instance=actual_post)
            return render(request, 'news/post_update.html', {'form': form})
    else:
        messages.warning(
            request, 'У вас нет прав на редaктирование этого поста')
        return redirect(actual_post)


@permission_required('news.add_post', raise_exception=True)
def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Новость добавлена')
            return redirect(new_post)
        else:
            messages.warning(request, 'Ошибка валидации')
            return redirect('add_post')
    else:
        form = AddPostForm()
    return render(request, 'news/add_post.html', {'form': form})


def page_search(request):
    search_query = request.GET.get('search', '')
    if search_query:
        selected_news = Post.objects.select_related('category', 'author').filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__full_name__icontains=search_query) |
            Q(category__title__icontains=search_query))
    else:
        selected_news = Post.objects.filter(
            is_published=True).select_related('category', 'author')

    context = {
        'selected_news': selected_news
    }
    context.update(get_pagination(request, selected_news))
    return context


def main_page(request):
    context = {}
    if request.user.is_authenticated:
        context.update(page_search(request))
        return render(request, 'base_news.html', context)
    return render(request, 'news/unauthorized_user.html')


def write_comment(request, form, selected_post):
    new_comment = form.save(commit=False)
    new_comment.user = request.user
    new_comment.post = selected_post
    new_comment.save()
    return new_comment


@login_required()
def full_news(request, pk):
    selected_post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(
        post=selected_post).select_related('post', 'user', 'parent')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            write_comment(request, form, selected_post)
            messages.success(request, 'Коментарий добавлен!!')
            return redirect(selected_post)
        else:
            messages.warning(request, 'Ошибка валидации')
            return redirect(selected_post)
    else:
        form = CommentForm()

    context = {'selected_post': selected_post,
               'comments': comments,
               'form': form
               }
    return render(request, 'news/full_news.html', context)


@login_required()
def category_news_list(request, pk):
    posts_selected_category = Post.objects.filter(
        category=pk).select_related('category', 'author')
    selected_category = Category.objects.get(pk=pk)
    context = {
        'selected_category': selected_category,
    }
    context.update(get_pagination(request, posts_selected_category))
    return render(request, 'news/category_news_list.html', context)


@login_required()
def author_news_list(request, pk):
    posts_selected_author = Post.objects.filter(
        author=pk).select_related('category', 'author')
    context = {}
    if posts_selected_author:
        name_author = posts_selected_author.first().author
        context = {
            'name_author': name_author,
        }
        context.update(get_pagination(request, posts_selected_author))
    return render(request, 'news/author_news_list.html', context)


@login_required()
def give_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            actual_user = request.user
            actual_user_message = form.cleaned_data['message']
            context = {
                'actual_user': actual_user,
                'actual_user_message': actual_user_message,
            }
            send_feedback_email(request, context)
            messages.success(request, 'Письмо отправлено!')
            return redirect('home')

        messages.warning(request, 'Ошибка отправки')
        return redirect('feedback')

    form = FeedbackForm()
    return render(request, 'news/feedback.html', {'form': form})
