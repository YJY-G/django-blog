from django.contrib import admin
from .models import Category, Post
from django_summernote.widgets import SummernoteWidget
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'summary': forms.Textarea(),
            'content': SummernoteWidget(),
        }

class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('title', 'slug', 'created_at', 'updated_at', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
