import os

from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)      # 제목은 문자열 30
    hook_text = models.CharField(max_length=100, blank=True)   # 미리보기 텍스트
    content = models.TextField()                 # 본문

    # 이미지 업로드
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)   # 이미지 저장 경로, 필수는 아님
    # %Y: 2022, %y: 22

    # 파일 업로드
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)          # 포스트 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)              # 포스트 수정 날짜

    # author는 나중에

    # pk는 자동으로 만들어짐
    def __str__(self):
        return f'[{self.pk}]{self.title}     {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'       # 블로그 게시물의 url

    # 업로드한 파일의 이름
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 파일의 확장자를 가져와서 파일 종류를 아이콘으로 표시하는 데에 사용
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]   # 가장 마지막 원소: 확장자