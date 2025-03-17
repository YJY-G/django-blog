from django.core.management.base import BaseCommand
from resume.models import Profile
from core.models import Post, Category  # 替换为你的实际 Post 模型
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = '创建模拟的博客文章数据'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='要创建的文章数量')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker(['zh_CN'])  # 使用中文数据
        
        # 确保有至少一个用户
        user = Profile.objects.first()
        if not user:
            user = user.objects.create_user(username='admin', password='admin')

        for i in range(count):
            # 生成随机日期
            created_date = datetime.now() - timedelta(days=random.randint(0, 365))
            
            post = Post.objects.create(
                title=fake.sentence(nb_words=6)[:-1],  # 去掉句号
                content='\n\n'.join(fake.paragraphs(nb=random.randint(3, 7))),
                author=user,
                created_at=created_date,
                status='published',
                slug=fake.slug(),
                category=Category.objects.first(),
                tags=fake.word(),
                summary=fake.sentence(nb_words=10)[:-1]
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created post: {post.title}')
            )