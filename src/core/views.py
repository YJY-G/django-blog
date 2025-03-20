from django.shortcuts import render
from .models import Post,Category,Comment
from django.forms import ModelForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from taggit.models import Tag
from django.shortcuts import redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json
import urllib.parse
from django.contrib import messages
from .utils import ContentFilter, get_client_ip, get_location_from_ip, CommentLimiter, check_content_quality
from django.conf import settings
from django.core.cache import cache

# Create your views here.

# 创建评论限制器实例
comment_limiter = CommentLimiter()
content_filter = ContentFilter()

def index(request):
    posts = Post.published.all()
    tag = request.GET.get('tag',None)
    if tag:
        try:
            tag_obj = Tag.objects.get(slug=tag)
            posts = posts.filter(tags__in=[tag_obj])
        except Tag.DoesNotExist:
            posts = posts
    # 处理分类筛选
    category_id = request.GET.get('category',None)
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    # 处理搜索
    q = request.GET.get('q',None)
    if q:
        posts = posts.filter(title__icontains=q)
    
    # 分页处理...
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
        html = render_to_string('post_list.html', {
            'page_obj': page_obj,
        }, request=request)
        return JsonResponse({'html': html})
    
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
    })



def details(request,slug:str):
    post = Post.published.get(slug=slug)
    post.views += 1
    post.save()
    
    try:
        next_post = post.get_next_by_created_at()
    except Post.DoesNotExist:
        next_post = post

    try:
        last_post = post.get_previous_by_created_at()
    except Post.DoesNotExist:
        last_post = post
        
    # 获取并解码 cookie 中的 name
    name = request.COOKIES.get('name')
    if name:
        try:
            name = urllib.parse.unquote(name)  # 解码 URL 编码的中文
        except:
            pass
    
    if request.method == 'POST':
        name = request.POST.get('name')
        body = request.POST.get('body')
        ip = get_client_ip(request)
        
        # 1. 检查是否被禁止评论
        if cache.get(f"banned_ip_{ip}"):
            return JsonResponse({
                'status': 'error',
                'message': '您已被禁止评论，请联系管理员',
                'is_valid': False
            })
        
        # 2. 检查评论频率限制
        can_comment, message = comment_limiter.can_comment(ip, body)
        if not can_comment:
            return JsonResponse({
                'status': 'error',
                'message': message,
                'is_valid': False
            })
        
        # 3. 检查内容质量
        is_valid_content, content_message = check_content_quality(body)
        if not is_valid_content:
            return JsonResponse({
                'status': 'error',
                'message': content_message,
                'is_valid': False
            })
        
        # 4. 内容审核
        is_valid, message, details = content_filter.check_text(body)
        
        if is_valid:
            # 增加评论计数
            comment_limiter.increment_counters(ip)
            
            # 创建评论
            comment = Comment(
                post=post,
                name=name,
                body=body,
                ip=ip,
                active=True
            )
            comment.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                comments = post.comments.filter(active=True)
                html = render_to_string(
                    'comments_list.html',
                    {'comments': comments},
                    request=request
                )
                
                response_data = {
                    'status': 'success',
                    'html': html,
                    'message': message,
                    'details': details,
                    'is_valid': is_valid
                }
                
                response = HttpResponse(
                    content=json.dumps(response_data, ensure_ascii=False),
                    content_type='application/json; charset=utf-8'
                )
                
                encoded_name = urllib.parse.quote(name)
                response.set_cookie('name', encoded_name, max_age=365*24*60*60)
                return response
    
    context = {
        'post': post,
        'next_post': next_post,
        'last_post': last_post,
        'categories': Category.objects.all(),
        'name': name,
        'comments': post.comments.filter(active=True),
    }
    
    return render(request, 'details.html', context)