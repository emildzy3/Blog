

from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', views.main_page, name='home'),
    # path('', cache_page(30)(views.main_page), name = 'home'),
    path('news/<int:pk>/', views.full_news, name='full_news'),
    path('news_category/<int:pk>/', views.category_news_list,
         name='category_news_list'),
    path('news_author/<int:pk>/', views.author_news_list, name='author_news_list'),
    path('author_full_list/', views.author_full_list, name='author_full_list'),
    path('feedback/', views.give_feedback, name='feedback'),
    path('add_post/', views.add_post, name='add_post'),
    path('post_update/<int:pk>/', views.post_update, name='post_update'),
    path('post_delete/<int:pk>/', views.post_delete, name='post_delete'),
]
