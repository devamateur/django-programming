import os
from django.contrib.auth.models import User
from django.db import models

# 다대다 관계 - Tag
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

# 다대일 관계 - Category
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)   # 카테고리는 unique해야 함
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):  # 객체에 대한 문자열 리턴
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:   # verbose_name_plural은 예약어
        verbose_name_plural = 'Categories'   # admin페이지의 Categorys대신 들어감
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
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # ForeignKey: 다대일 관계 표현
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    # pk는 자동으로 만들어짐
    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author} : {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'       # 블로그 게시물의 url

    # 업로드한 파일의 이름
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 파일의 확장자를 가져와서 파일 종류를 아이콘으로 표시하는 데에 사용
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]   # 가장 마지막 원소: 확장자