

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomReaderCreationForm, CustomUserChangeForm
from .models import ProfileAuthor
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomReaderCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('id', 'email', 'full_name', 'is_active', 'is_author')
    list_filter = ('email', 'full_name', 'is_active', 'is_author')
    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'photo', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_author',
                         'date_joined', 'groups')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'photo', 'password1', 'password2',
                       'is_staff', 'is_active', 'is_author', 'groups',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    list_display_links = ('id', 'email')
    list_editable = ('is_author',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(ProfileAuthor)
