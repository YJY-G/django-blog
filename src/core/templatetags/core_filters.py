from django import template

register = template.Library()

@register.filter
def active_comments(comments):
    """只返回激活状态的评论"""
    if hasattr(comments, 'filter'):  # 检查是否是 QuerySet  
        return comments.filter(active=True)
    return []  # 如果不是 QuerySet，返回空列表

@register.filter
def comment_count(queryset):
    """返回激活状态的评论数量"""
    if hasattr(queryset, 'filter'):  # 检查是否是 QuerySet
        return queryset.filter(active=True).count()
    return 0  # 如果不是 QuerySet，返回 0