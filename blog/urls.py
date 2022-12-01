from django.urls import path
from . import views

urlpatterns = [   # IP주소/blog/

    ### CBV(Class Based View)  이용
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),       # 댓글
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),        # comment의 pk
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),              # post의 pk
    path('create_post/', views.PostCreate.as_view()),
    path('category/<str:slug>/', views.category_page),    # IP주소/blog/category/slug/

    path('tag/<str:slug>/', views.tag_page),                # IP주소/blog/tag/slug/
    path('search/<str:q>/', views.PostSearch.as_view()),

    ### FBV(Function Based View) 이용
    #path('', views.index),    # IP주소/blog/
    #path('<int:pk>/', views.single_post_page)  # int형의 pk가 url로 들어온다..
]