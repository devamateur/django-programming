from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Post, Category

class PostList(ListView):
    model = Post
    ordering = '-pk'   # pk로 내림차순으로 정렬(최신순)

    # PostList에서 사용할 데이터를 넘겨줌(여기서는 카테고리)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count

        return context

    # 템플릿은 모델명_list.html이 자동으로 불려짐 -> post_list.html
    # 전달되는 매개변수(FBV render() 세 번째 매개변수): 모델명_list -> post_list
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count

        return context
    # 템플릿 -> post_detail.html이 자동으로 불려짐
    # 전달되는 매개변수: 모델명 -> post

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        # 특정 slug를 갖는 카테고리
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(request, 'blog/post_list.html', {
        'category': category,
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })
""" FBV """
#def index(request):
#    posts = Post.objects.all().order_by('-pk')     # 모든 post를 가져옴, pk기준으로 최신순으로 정렬(내림차순)
#    return render(request, 'blog/index.html', {'posts': posts})    # 템플릿이 호출될 때 posts 변수도 같이 넘김

#def single_post_page(request, pk):
#    post = Post.objects.get(pk=pk)      # 특정 pk의 post만 가져 옴
#    return render(request, 'blog/single_post_page.html', {'post':post})