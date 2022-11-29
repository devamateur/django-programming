from django.shortcuts import render

# Create your views here.
from blog.models import Post


def landing(request):
    recent_post = Post.objects.order_by('-pk')[:3]      # 포스트를 최신순으로 3개 가져 옴
    return render(request, 'single_pages/landing.html', {
        'recent_posts': recent_post,
    })

def about_me(request):
    return render(request, 'single_pages/about_me.html')