from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
# 테스트 코드
class TestView(TestCase):
    def setUp(self):   # setUp 함수, 테스트 코드 수행 전 설정하는 작업..
        self.client = Client()

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
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)     # navbar안에 Blog메뉴가 있는지
        self.assertIn('About Me', navbar.text)  # About Me 메뉴가 있는지

        # post가 정상적으로 보이는지
        # 1) 맨 처음에는 post가 없음(게시물이 0개)
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id='main-area')   # id가 main-area인 div태그
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 2) post가 추가되는 경우
        post_001 = Post.objects.create(title="첫 번째 포스트", content="첫 번째 포스트입니다.")
        post_002 = Post.objects.create(title="두 번째 포스트", content="두 번째 포스트입니다.")
        self.assertEqual(Post.objects.count(), 2)

        # post가 추가된 경우, 본문 내용을 테스트
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)   # response의 status코드가 200인지
        soup = BeautifulSoup(response.content, 'html.parser')   # html 파싱
        main_area = soup.find('div', id='main-area')   # id가 main-area인 div태그
        self.assertIn(post_001.title, main_area.text)   # post의 제목이 본문에 존재하는지
        self.assertIn(post_002.title, main_area.text)   # post의 제목이 본문에 존재하는지
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

    # 상세 페이지 테스트
    def test_post_detail(self):
        post_001 = Post.objects.create(title="첫 번째 포스트", content="첫 번째 포스트입니다.")
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')    # post의 url 주소 확인

        # 응답 확인(html이 잘 가져와졌는지..)
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)   # response의 status코드가 200인지

        soup = BeautifulSoup(response.content, 'html.parser')   # html 파싱

        # navbar가 정상적으로 보이는지
        # assertIn(a, b): a가 b에 포함되는지
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)  # navbar안에 Blog메뉴가 있는지
        self.assertIn('About Me', navbar.text)  # About Me 메뉴가 있는지

        self.assertIn(post_001.title, soup.title.text)   # title태그에 포스트 제목이 포함되어있는지 확인
        main_area = soup.find('div', id='main-area')   # id가 main-area인 div태그를 찾음
        post_area = main_area.find('div', id='post-area')   # main_area안에 있는 post-area를 찾음
        self.assertIn(post_001.title, post_area.text)
        self.assertIn(post_001.content, post_area.text)
