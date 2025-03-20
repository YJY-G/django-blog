from django.contrib import admin
from .models import Category, Post,Comment
from markdownx.admin import MarkdownxModelAdmin


class PostAdmin(MarkdownxModelAdmin):
    class Media:
        css = {
            'all': ('css/pygments-monokai.css',)
        }
        js = ('admin/js/markdownx-enhance.js',
              'admin/js/markdownx-clipboard.js',
              )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'ip','active','created_at')
    list_filter = ('active','created_at')
    ordering = ('-created_at',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)


