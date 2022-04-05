

from django.urls import path
from . import views


urlpatterns = [
    path('registration_reader/', views.registration_reader, name='registration'),
    path('registration_author', views.apply_for_registration,
         name='apply_for_registration'),
    path('registration_for_author', views.registration_for_author,
         name='registration_for_author'),
    path('authorization/', views.authorizationUser, name='authorization'),
    path('logout/', views.logoutUser, name='logoutUser'),

    path('reset_password/', views.PasswordResetViewCustom.as_view(),
         name='password_reset'),
    path('reset_password_from_email/',
         views.PasswordResetDoneViewCustom.as_view(), name='password_reset_done'),
    path('reset_password_new/<uidb64>/<token>/',
         views.PasswordResetConfirmViewCustom.as_view(),
         name='password_reset_confirm'),
    path('reset_password_success/', views.PasswordResetCompleteViewCustom.as_view(),
         name='password_reset_complete'),

    path('confirm_email/', views.sending_email_confirmation, name='confirm_email'),
    path('activation/<uidb64>/<token>/', views.activate_reader, name='activation'),
    path('user_is_not_found/', views.user_is_not_found, name='user_is_not_found'),

    path('profile/', views.get_profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),

    path('author_profile/<int:pk>/', views.get_author_profile,
         name='author_profile'),

]
