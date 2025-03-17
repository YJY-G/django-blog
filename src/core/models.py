from django.db import models
from resume.models import Profile
# Create your models here.

class Category(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-order', 'id']
        verbose_name = '日志分类'
        verbose_name_plural = '日志分类'


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='created_at')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='images/posts/', null=True, blank=True,default='https://picsum.photos/800/400')
    summary = models.CharField(max_length=255, blank=True)
    
    tags = models.CharField(max_length=255)

    views = models.PositiveIntegerField(default=0)
    flag = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=[('draft', '草稿'), ('published', '发布'), ('archived', '归档')], default='draft')

    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')]
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '日志'
        verbose_name_plural = '日志'
    