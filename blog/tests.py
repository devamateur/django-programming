from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User

# Create your tests here.
# 테스트 코드
class TestView(TestCase):
    def setUp(self):   # setUp 함수, 테스트 코드 수행 전 설정하는 작업..
        self.client = Client()
        self.user_kim = User.objects.create_user(username="kim", password="mypassword")
        self.user_lee = User.objects.create_user(username="lee", password="mypassword")

        # 카테고리
        self.category_com = Category.objects.create(name="computer", slug="computer")
        self.category_edu = Category.objects.create(name="education", slug="education")

        self.post_001 = Post.objects.create(title="첫 번째 포스트", content="첫 번째 포스트입니다.",
                                       author=self.user_kim, category=self.category_com)
        self.post_002 = Post.objects.create(title="두 번째 포스트", content="두 번째 포스트입니다.",
                                       author=self.user_lee, category=self.category_edu)
        self.post_003 = Post.objects.create(title="세 번째 포스트", content="세 번째 포스트입니다.",
                                            author=self.user_lee)
    def nav_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)  # navbar안에 Blog메뉴가 있는지
        self.assertIn('About Me', navbar.text)  # About Me 메뉴가 있는지

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')     # 홈 링크 확인

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')  # 블로그 링크 확인

        about_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_btn.attrs['href'], '/about_me/')  # About Me 링크 확인

    def category_test(self, soup):
        category_card = soup.find('div', id='category_card')   # 사이드바
        self.assertIn('Categories', category_card.text)

        # f string: 카테고리 (포스트수)의 형태
        # category_com.post_set: 해당 카테고리와 연결된 post의 집합을 가져옴
        self.assertIn(f'{self.category_com.name} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_edu.name} ({self.category_edu.post_set.count()})', category_card.text)
        self.assertIn(f'미분류 (1)', category_card.text)


    # 포스트 목록 테스트
    def test_post_list(self):
        response = self.client.get('/blog/')
        ' response 결과가 정상적인 화면인지 테스트 '
        self.assertEqual(response.status_code, 200)   # response의 status코드가 200인지

        soup = BeautifulSoup(response.content, 'html.parser')   # html 파싱

        # title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'Blog')   # title 태그 안에 있는 텍스트가 Blog인지

        # navbar가 정상적으로 보이는지
        # assertIn(a, b): a가 b에 포함되는지
        self.nav_test(soup)
        self.category_test(soup)

        self.assertEqual(Post.objects.count(), 3)

        # post가 추가된 경우, 본문 내용을 테스트
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)  # response의 status코드가 200인지
        soup = BeautifulSoup(response.content, 'html.parser')  # html 파싱
        main_area = soup.find('div', id='main-area')  # id가 main-area인 div태그
        self.assertIn(self.post_001.title, main_area.text)  # post의 제목이 본문에 존재하는지
        self.assertIn(self.post_002.title, main_area.text)  # post의 제목이 본문에 존재하는지
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        # author 확인
        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)

        # post가 정상적으로 보이는지
        # 1) 맨 처음에는 post가 없음(게시물이 0개)
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)  # response의 status코드가 200인지
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')   # id가 main-area인 div태그
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 2) post가 추가되는 경우
        #post_001 = Post.objects.create(title="첫 번째 포스트", content="첫 번째 포스트입니다.",
        #                               author=self.user_kim)
        #post_002 = Post.objects.create(title="두 번째 포스트", content="두 번째 포스트입니다.",
        #                               author=self.user_lee)


    # 상세 페이지 테스트
    def test_post_detail(self):
        post_001 = Post.objects.create(title="첫 번째 포스트", content="첫 번째 포스트입니다.",
                                       author=self.user_kim)
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')    # post의 url 주소 확인

        # 응답 확인(html이 잘 가져와졌는지..)
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)   # response의 status코드가 200인지

        soup = BeautifulSoup(response.content, 'html.parser')   # html 파싱

        # navbar가 정상적으로 보이는지
        # assertIn(a, b): a가 b에 포함되는지
        self.nav_test(soup)

        self.assertIn(post_001.title, soup.title.text)   # title태그에 포스트 제목이 포함되어있는지 확인
        main_area = soup.find('div', id='main-area')   # id가 main-area인 div태그를 찾음
        post_area = main_area.find('div', id='post-area')   # main_area안에 있는 post-area를 찾음
        self.assertIn(post_001.title, post_area.text)
        self.assertIn(post_001.content, post_area.text)
        self.assertIn(post_001.author.username.upper(), post_area.text)
