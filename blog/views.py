from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Category, Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

# 포스트 수정을 위한 클래스
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']
    template_name = 'blog/post_update_form.html'      # 템플릿을 호출

    # 포스트를 작성한 유저 확인
    def dispatch(self, request, *args, **kwargs):
        # request 유저와 post를 작성한 유저가 같은지 확인
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied          # PermissionDenied exception 발생시킴

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count

        return context
# 포스트 생성을 위한 클래스
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    # 모델명_form.html이 자동으로 호출

    # 슈퍼유저 or 스태프유저에게 접근권한 부여(모델에 대한)
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user            # 현재 post를 생성하는 유저
        if current_user.is_authenticated and \
                (current_user.is_superuser or self.request.user.is_staff):            # 해당 유저가 인증된 유저이면
            form.instance.author = current_user     # 폼의 authorm를 해당 유저로
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')        #인증되지 않은 사용자일 경우 그냥 redirect

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count

        return context
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

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()          # tag값을 가진 포스트 집합

    return render(request, 'blog/post_list.html', {
        'tag': tag,
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