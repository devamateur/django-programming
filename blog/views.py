from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Post

class PostList(ListView):
    model = Post
    ordering = '-pk'   # pk로 내림차순으로 정렬(최신순)
    # 템플릿은 모델명_list.html이 자동으로 불려짐 -> post_list.html
class PostDetail(DetailView):
    model = Post
    # 템플릿 -> post_detail.html이 자동으로 불려짐

""" FBV """
#def index(request):
#    posts = Post.objects.all().order_by('-pk')     # 모든 post를 가져옴, pk기준으로 최신순으로 정렬(내림차순)
#    return render(request, 'blog/index.html', {'posts': posts})    # 템플릿이 호출될 때 posts 변수도 같이 넘김

#def single_post_page(request, pk):
#    post = Post.objects.get(pk=pk)      # 특정 pk의 post만 가져 옴
#    return render(request, 'blog/single_post_page.html', {'post':post})