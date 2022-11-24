from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Category, Tag, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

# 포스트 수정을 위한 클래스
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']  # , 'tags'
    template_name = 'blog/post_update_form.html'      # 템플릿을 호출

    # 포스트를 작성한 유저 확인
    def dispatch(self, request, *args, **kwargs):
        # request 유저와 post를 작성한 유저가 같은지 확인
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied          # PermissionDenied exception 발생시킴

    # post방식으로 전달하면 form_valid()가 필요함
    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')  # post_form의 tags_str을 가져옴
        if tags_str:
            tags_str = tags_str.strip()  # 문자열의 앞 뒤 공백 제거
            tags_str = tags_str.replace(',', ';')  # 구분자(delimiter) ;로 통일
            tags_list = tags_str.split(';')  # ex) 'internet; programming;' -> 'internet' 'programming'

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)  # 문자열에 해당하는 태그 객체 없으면 create 있으면 가져옴
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)  # 새로 생성된 태그의 경우, 슬러그 생성
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()

        # 기존 post에 tag가 있는 경우
        if self.object.tags.exists:
            tag_str_list = list()
            for t in self.object.tags.all():
                tag_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tag_str_list)
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
            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')     # post_form의 tags_str을 가져옴
            if tags_str:
                tags_str = tags_str.strip()     # 문자열의 앞 뒤 공백 제거
                tags_str = tags_str.replace(',', ';')      # 구분자(delimiter) ;로 통일
                tags_list = tags_str.split(';')            # ex) 'internet; programming;' -> 'internet' 'programming'

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)       # 문자열에 해당하는 태그 객체 없으면 create 있으면 가져옴
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)           # 새로 생성된 태그의 경우, 슬러그 생성
                        tag.save()
                    self.object.tags.add(tag)
            return response
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
    paginate_by = 5     # 한 페이지에 5개씩 보여줌

    # PostList에서 사용할 데이터를 넘겨줌(여기서는 카테고리)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count

        return context

    # 템플릿은 모델명_list.html이 자동으로 불려짐 -> post_list.html
    # 전달되는 매개변수(FBV render() 세 번째 매개변수): 모델명_list -> post_list


class PostSearch(PostList):  # ListView 상속, post_list, post_list.html
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']            # 검색어(query)를 가져 옴

        # 포스트 제목과 태그에 대해 검색
        post_list = Post.objects.filter(Q(title__contains=q) | Q(tags__name__contains=q)).distinct()

        return post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        context['comment_form'] = CommentForm
        return context
    # 템플릿 -> post_detail.html이 자동으로 불려짐
    # 전달되는 매개변수: 모델명 -> post

# 댓글 등록하는 메소드
def new_comment(request, pk):
    if request.user.is_authenticated:       # 로그인한 유저인가
        post = get_object_or_404(Post, pk=pk)       # 해당 댓글이 달린 포스트 가져옴
        if request.method == 'POST':                # 새로 댓글을 작성하는 경우
            comment_form = CommentForm(request.POST)        # POST로 전달받은 내용
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)   # 모델에 등록(commit)은 하지 않음
                comment.post = post
                comment.author = request.user
                comment.save()              # 모델에 등록
                return redirect(comment.get_absolute_url())
        else:   # request.method == 'GET'인 경우
            return redirect(post.get_absolute_url())
    else:       # 로그인하지 않은 유저인 경우
        raise PermissionDenied

# 댓글 수정을 위한 뷰
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    # 템플릿 이름: comment_form
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        # request 유저와 comment를 작성한 유저가 같은지 확인
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied          # PermissionDenied exception 발생시킴

    # 템플릿 이름: comment_form


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