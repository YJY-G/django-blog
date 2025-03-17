from django.shortcuts import render
from .models import Post,Category
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.

def index(request):
    posts = Post.objects.all()
    
    # 处理分类筛选
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    # 处理搜索
    q = request.GET.get('q')
    if q:
        posts = posts.filter(title__icontains=q)
    
    # 分页处理...
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('post_list.html', {
            'page_obj': page_obj,
        }, request=request)
        return JsonResponse({'html': html})
    
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
    })


def details(request,pid:int):
    post = Post.objects.get(id=pid)
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
    return render(request, 'details.html',{'post':post,"next_post":next_post,"last_post":last_post})