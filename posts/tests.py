from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='matt', password='pass')

    def test_can_list_posts(self):
        matt = User.objects.get(username='matt')
        Post.objects.create(owner=matt, title='a test title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_a_post(self):
        self.client.login(username='matt', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a test title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        matt = User.objects.create_user(username='matt', password='pass')
        kev = User.objects.create_user(username='kev', password='pass')
        Post.objects.create(
            owner=matt, title='a title', content='matts content'
        )
        Post.objects.create(
            owner=kev, title='another title', content='kevs content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_fetch_a_post_with_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_posts(self):
        self.client.login(username='matt', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_cant_update_a_post_they_dont_own(self):
        self.client.login(username='matt', password='pass')
        response = self.client.put('/posts/2/', {'title': 'any title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
