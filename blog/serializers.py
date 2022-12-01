from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )         # 외래키 필드 값을 가져올 때 ()로 표현

class postSerializer(serializers.ModelSerializer):
    # author 설정
    author = userSerializer(many=False, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'created_at']