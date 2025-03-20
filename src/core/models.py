from django.db import models
from resume.models import Profile
from taggit.managers import TaggableManager
from markdownx.utils import markdownify
from markdownx.models import MarkdownxField
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


class PublishedManager(models.Manager):
    """自定义模型管理器"""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')



class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='created_at')
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='images/posts/', null=True, blank=True,default='https://picsum.photos/800/400')
    summary = models.CharField(max_length=255, blank=True)
    
    # tags = models.CharField(max_length=255)
    tags = TaggableManager("标签",blank=True)
    views = models.PositiveIntegerField(default=0)
    flag = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=[('draft', '草稿'), ('published', '发布')], default='draft')

    def __str__(self):
        return self.title
    
    # def get_tags_list(self):
    #     return [tag.strip() for tag in self.tags.split(',')]
    def formatted_content(self):
        return markdownify(self.content)
    
    # 自定义模型管理器
    objects = models.Manager()
    # 发布状态管理器
    published = PublishedManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = '日志'
        verbose_name_plural = '日志'



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=120)
    ip = models.CharField(max_length=50, blank=True)
    body = models.TextField()
    active = models.BooleanField("有效",default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} 评论了 {self.post.title}'
    
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'
        indexes = [
            models.Index(fields=['ip','created_at']),
        ]