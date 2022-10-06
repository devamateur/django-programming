from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)      # 제목은 문자열 30
    content = models.TextField()                 # 본문

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)   # 이미지 저장 경로, 필수는 아님
    # %Y: 2022, %y: 22

    created_at = models.DateTimeField(auto_now_add=True)          # 포스트 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)              # 포스트 수정 날짜

    # author는 나중에

    # pk는 자동으로 만들어짐
    def __str__(self):
        return f'[{self.pk}]{self.title}     {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'       # 블로그 게시물의 url
