from aip import AipContentCensor
import requests
def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location_from_ip(ip):
    """获取IP地址对应的地理位置"""
    if ip in ['127.0.0.1', 'localhost']:
        return '本地测试'
        
    try:
        # 使用 ip-api.com 的免费服务
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        
        if data['status'] == 'success':
            # 返回 "国家 城市" 格式
            location = []
            if data.get('country'):
                location.append(data['country'])
            if data.get('city'):
                location.append(data['city'])
            return ' '.join(location) if location else '未知地区'
        return '未知地区'
    except:
        return '未知地区'

class ContentFilter:
    def __init__(self):
        # 替换为你的百度API密钥
        self.APP_ID = '6613568'
        self.API_KEY = 'Ux7qQh9DuIfkDQjepk1A8BUV'
        self.SECRET_KEY = 'HZPd64tfEpp6gQtXKFYgqJsu78F8KEH5'
        self.client = AipContentCensor(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def check_text(self, text):
        try:
            result = self.client.textCensorUserDefined(text)
            # conclusionType: 1:合规, 2:不合规, 3:疑似
            if result.get('conclusionType') == 1:
                return True, "评论已发布", None
            else:
                # 获取具体的违规原因
                msg = "评论包含以下问题："
                details = []
                for item in result.get('data', []):
                    details.append(item.get('msg', ''))
                return False, msg, details
        except Exception as e:
            return False, "评论审核失败，请稍后重试", None
        

from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache

class CommentLimiter:
    def __init__(self):
        self.minute_limit = 3  # 每分钟最大评论数
        self.hour_limit = 20   # 每小时最大评论数
        self.day_limit = 100   # 每天最大评论数
        self.min_interval = 10 # 两次评论之间的最小间隔(秒)
        self.min_length = 3    # 评论最小长度
        self.max_length = 500  # 评论最大长度
        
    def _get_cache_key(self, ip, period):
        return f"comment_limit_{ip}_{period}"
        
    def can_comment(self, ip, content):
        now = timezone.now()
        
        # 1. 检查评论长度
        if len(content) < self.min_length:
            return False, f"评论内容太短，至少{self.min_length}个字符"
        if len(content) > self.max_length:
            return False, f"评论内容太长，最多{self.max_length}个字符"
            
        # 2. 检查评论间隔
        last_comment_time = cache.get(f"last_comment_{ip}")
        if last_comment_time:
            time_passed = (now - last_comment_time).total_seconds()
            if time_passed < self.min_interval:
                return False, f"评论太频繁，请{self.min_interval-int(time_passed)}秒后再试"
        
        # 3. 检查各时间段的评论数量
        periods = {
            'minute': (self.minute_limit, timedelta(minutes=1)),
            'hour': (self.hour_limit, timedelta(hours=1)),
            'day': (self.day_limit, timedelta(days=1))
        }
        
        for period, (limit, delta) in periods.items():
            cache_key = self._get_cache_key(ip, period)
            count = cache.get(cache_key, 0)
            
            if count >= limit:
                return False, f"评论次数超出限制，请稍后再试"
        
        return True, "可以评论"
    
    def increment_counters(self, ip):
        now = timezone.now()
        
        # 更新最后评论时间
        cache.set(f"last_comment_{ip}", now, timeout=86400)  # 24小时过期
        
        # 更新各时间段计数器
        periods = {
            'minute': 60,    # 60秒
            'hour': 3600,    # 1小时
            'day': 86400     # 24小时
        }
        
        for period, timeout in periods.items():
            cache_key = self._get_cache_key(ip, period)
            count = cache.get(cache_key, 0)
            cache.set(cache_key, count + 1, timeout=timeout)

# 创建一个检查内容的函数
def check_content_quality(content):
    # 检查重复字符
    for char in set(content):
        if content.count(char) > len(content) * 0.4:
            return False, "包含过多重复字符"
    
    # 检查特殊字符比例
    special_chars = sum(1 for c in content if not c.isalnum() and not c.isspace())
    if special_chars / len(content) > 0.3:
        return False, "特殊字符比例过高"
    
    return True, "内容格式正常"