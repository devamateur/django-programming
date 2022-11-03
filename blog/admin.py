from django.contrib import admin
from .models import Post, Category, Tag

# Register your models here.

admin.site.register(Post)   # admin에 Post 모델 등록

# name필드 값으로 slug 자동 생성
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}   # 카테고리가 자동으로 slug로 만들어짐?
admin.site.register(Category, CategoryAdmin)  # Category도 등록

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Tag, TagAdmin)                        # Tag도 등록