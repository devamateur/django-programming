from django.urls import path
from . import views

urlpatterns = [   # IP주소/blog/

    ### CBV(Class Based View)  이용
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.category_page)
    ### FBV(Function Based View) 이용
    #path('', views.index),    # IP주소/blog/
    #path('<int:pk>/', views.single_post_page)  # int형의 pk가 url로 들어온다..
]