

from django.contrib import admin
from .models import Post, Category, Comment
from mptt.admin import MPTTModelAdmin


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_creation', 'category',
                    'is_published', 'preview_photo', 'author')
    list_filter = ('category', 'is_published', 'author')
    list_editable = ('is_published',)
    readonly_fields = ('date_creation', 'date_change')
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'category', 'preview_photo', 'author',)
        }),
        ('Advanced options', {
            'fields': ('is_published', 'date_creation', 'date_change'),
        }),
    )
    search_fields = ('title', 'content')

    list_display_links = ('id', 'title')


class DisplayingCommentAdmin(MPTTModelAdmin):
    list_display = ('comment_text', 'level', 'publication_date', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Comment, DisplayingCommentAdmin)
