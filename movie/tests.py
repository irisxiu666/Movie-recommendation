from django.test import TestCase, Client
from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from unittest.mock import patch, MagicMock  # Import patch from unittest.mock
from movie.ajax_views import login, get_user, register, movies, search_movies, collect, decollect, make_comment, \
    personal, my_comments, delete_comment, my_rate, delete_rate, mycollect


class UrlsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_admin_url(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Assuming admin redirects to login if not authenticated

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)  # Assuming login view returns HTTP 200 OK

    def test_register_url(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)  # Assuming register view returns HTTP 200 OK

    def test_get_user_url(self):
        response = self.client.get(reverse('get_user'))
        self.assertEqual(response.status_code, 200)  # Assuming get_user view returns HTTP 200 OK

    def test_media_url(self):
        response = self.client.get('/media/')  # Assuming MEDIA_URL is '/media/'
        self.assertEqual(response.status_code, 404)  # Assuming there's no view associated with the media URL

    def test_static_url(self):
        response = self.client.get('/static/')  # Assuming STATIC_URL is '/static/'
        self.assertEqual(response.status_code, 404)  # Assuming there's no view associated with the static URL

    def test_all_tags_url(self):
        response = self.client.get(reverse('all_tags'))
        self.assertEqual(response.status_code, 200)  # Assuming all_tags view returns HTTP 200 OK

    def test_delete_rate_url(self):
        response = self.client.get(reverse('delete_rate', args=[1]))  # Assuming delete_rate view requires a rate_id
        self.assertEqual(response.status_code, 200)  # Assuming delete_rate view returns HTTP 200 OK


class LoginTestCase(TestCase):
    def test_successful_login(self):
        # Mock request object with JSON data
        request = HttpRequest()
        request.method = 'POST'
        request.json = {'username': 'test_user', 'password': 'test_password'}

        # Mock User.objects.filter() and User.objects.get() methods
        with patch('movie.models.User.objects') as mock_user_objects:
            mock_user_objects.filter.return_value.exists.return_value = True

            response = login(request)
            self.assertEqual(response.status_code, 200)

    def test_wrong_password(self):
        request = HttpRequest()
        request.method = 'POST'
        request.json = {'username': 'test_user', 'password': 'wrong_password'}

        with patch('movie.models.User.objects') as mock_user_objects:
            mock_user_objects.filter.return_value.exists.return_value = True
            mock_user_objects.get.return_value.password = 'test_password'

            response = login(request)
            self.assertEqual(response.content, b'{"Code": 400, "Msg": "Wrong password", "Data": "error"}')

    def test_non_existing_account(self):
        request = HttpRequest()
        request.method = 'POST'
        request.json = {'username': 'non_existing_user', 'password': 'test_password'}

        with patch('movie.models.User.objects') as mock_user_objects:
            mock_user_objects.filter.return_value.exists.return_value = False

            response = login(request)
            self.assertEqual(response.content, b'{"Code": 400, "Msg": "Wrong password", "Data": "error"}')

class GetUserTestCase(TestCase):
    def test_get_user_success(self):
        # Mock request object with access-token header
        request = HttpRequest()
        #request.headers["access-token"] = "dummy_access_token"

        # Mock User.objects.filter().first() method
        with patch('movie.models.User.objects.filter') as mock_filter:
            # Mock user object returned by filter().first()
            mock_user = MagicMock()
            mock_user.username = "test_user"
            mock_user.role = []
            mock_user.is_superuser = True
            mock_filter.return_value.first.return_value = mock_user

            # Call the view function
            response = get_user(request)
            # Check the response
            self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": {"name": "test_user", "role": [], "isSuperuser": true}}')

    def test_get_user_failure(self):
        # Mock request object without access-token header
        request = HttpRequest()

        # Mock User.objects.filter().first() method
        with patch('movie.models.User.objects.filter') as mock_filter:
            # Mock filter().first() to return None
            mock_filter.return_value.first.return_value = None

            # Call the view function
            response = get_user(request)
            # Check the response
            self.assertEqual(response.content, b'{"Code": 400, "Msg": "\\u5931\\u8d25", "Data": "error"}')

class RegisterTestCase(TestCase):
    def test_register_success(self):
        # Mock request object with JSON data
        request = HttpRequest()
        request.json = {
            'username': 'test_user',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'test@example.com'
        }

        # Mock User.objects.filter().exists() method
        with patch('movie.models.User.objects.filter') as mock_filter:
            mock_filter.return_value.exists.return_value = False

            # Mock User.objects.create() method
            with patch('movie.models.User.objects.create') as mock_create:
                mock_create.return_value.id = 123  # Mock the created user's ID

                # Call the view function
                response = register(request)
                # Check the response
                self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": 123}')

    def test_register_incomplete_information(self):
        # Mock request object with incomplete JSON data
        request = HttpRequest()
        request.json = {'username': 'test_user'}

        # Call the view function
        response = register(request)
        # Check the response
        self.assertEqual(response.content, b'{"Code": 400, "Msg": "Incomplete information", "Data": "error"}')

    def test_register_inconsistent_passwords(self):
        # Mock request object with JSON data and inconsistent passwords
        request = HttpRequest()
        request.json = {
            'username': 'test_user',
            'password1': 'password123',
            'password2': 'password456'  # Different password here
        }

        # Call the view function
        response = register(request)
        # Check the response
        self.assertEqual(response.content, b'{"Code": 400, "Msg": "inconsistent passwords", "Data": "error"}')


    def test_register_account_already_exists(self):
        # Mock request object with JSON data
        request = HttpRequest()
        request.json = {
            'username': 'existing_user',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'existing@example.com'
        }

        # Mock User.objects.filter().exists() to return True
        with patch('movie.models.User.objects.filter') as mock_filter:
            mock_filter.return_value.exists.return_value = True

            # Call the view function
            response = register(request)
            # Check the response
            self.assertEqual(response.content, b'{"Code": 400, "Msg": "Account already exits", "Data": "error"}')



class MoviesTestCase(TestCase):
    def test_movies_default_order(self):
        # Mock request object with default JSON data
        request = HttpRequest()
        request.json = {}

        # Mock Movie.objects.order_by() method
        with patch('movie.models.Movie.objects.order_by') as mock_order_by:
            mock_order_by.return_value = []  # Mock an empty queryset

            # Call the view function
            response = movies(request)
            print(response.content)
            # Check the response
            self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": {"total": 0, "results": []}}')
            # Assuming default order is by popularity (order_by('-id'))
            mock_order_by.assert_called_once_with('-id')

    def test_movies_collection_order(self):
        # Mock request object with JSON data specifying order by collection
        request = HttpRequest()
        request.json = {'order': 'collect'}

        # Mock Movie.objects.annotate().order_by() method
        with patch('movie.models.Movie.objects.annotate') as mock_annotate:
            mock_annotate.return_value.order_by.return_value = []  # Mock an empty queryset

            # Call the view function
            response = movies(request)

            # Check the response
            print(response.content)
            # Check the response
            self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": {"total": 0, "results": []}}')

            # Assuming order by collection (order_by('-collectors'))
            mock_annotate.assert_called_once()
            mock_annotate.return_value.order_by.assert_called_once_with('-collectors')

    # Add similar tests for other order options (rate, years)

    def test_movies_filter_by_tag(self):
        # Mock request object with JSON data specifying tag
        request = HttpRequest()
        request.json = {'tag': 1}  # Assuming tag ID is 1

        # Mock Movie.objects.filter().order_by() method
        with patch('movie.models.Movie.objects.filter') as mock_filter:
            mock_filter.return_value.order_by.return_value = []  # Mock an empty queryset

            # Call the view function
            response = movies(request)

            # Check the response
            print(response.content)
            # Check the response
            self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": {"total": 0, "results": []}}')


class SearchMoviesTestCase(TestCase):
    def test_search_movies_no_keyword(self):
        # Mock request object with JSON data and no keyword
        request = HttpRequest()
        request.json = {}

        # Mock Movie.objects.filter().order_by() method
        with patch('movie.models.Movie.objects.filter') as mock_filter:
            mock_filter.return_value.order_by.return_value = []  # Mock an empty queryset

            # Call the view function
            response = search_movies(request)
            # Check the response
            self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": []}')

    def test_search_movies_with_keyword(self):
        # Mock request object with JSON data and keyword
        request = HttpRequest()
        request.json = {'keyword': 'action'}

        # Mock Movie.objects.filter().order_by() method
        with patch('movie.models.Movie.objects.filter') as mock_filter:
            mock_filter.return_value.order_by.return_value = []  # Mock an empty queryset

            # Call the view function
            response = search_movies(request)

            print(response.content)
            # Check the response
            self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": []}')


class CollectDecollectTestCase(TestCase):
    def setUp(self):
        self.user = MagicMock()
        self.movie_id = 1

    def test_collect(self):
        # Mock request object with a user
        request = HttpRequest()
        request.user_ = self.user

        # Mock Movie.objects.get() method
        with patch('movie.models.Movie.objects.get') as mock_get:
            movie_instance = MagicMock()
            mock_get.return_value = movie_instance

            # Call the view function
            response = collect(request, movie_id=self.movie_id)
            # Check the response
            self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": "success"}')
            movie_instance.collect.add.assert_called_once_with(self.user)
            movie_instance.save.assert_called_once()

    def test_decollect(self):
        # Mock request object with a user
        request = HttpRequest()
        request.user_ = self.user

        # Mock Movie.objects.get() method
        with patch('movie.models.Movie.objects.get') as mock_get:
            movie_instance = MagicMock()
            mock_get.return_value = movie_instance

            # Call the view function
            response = decollect(request, movie_id=self.movie_id)

            # Check the response
            self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": "success"}')
            movie_instance.collect.remove.assert_called_once_with(self.user)
            movie_instance.save.assert_called_once()

class MakeCommentPersonalTestCase(TestCase):
    def setUp(self):
        self.user = MagicMock()
        self.movie_id = 1
        self.comment_content = "Test comment"

    def test_make_comment(self):
        # Mock request object with a user and JSON data
        request = HttpRequest()
        request.user_ = self.user
        request.json = {'comment': self.comment_content}

        # Mock Movie.objects.get() method
        with patch('movie.models.Movie.objects.get') as mock_get:
            movie_instance = MagicMock()
            mock_get.return_value = movie_instance

            # Mock Comment.objects.create() method
            with patch('movie.models.Comment.objects.create') as mock_create:
                # Call the view function
                response = make_comment(request, movie_id=self.movie_id)
                # Check the response
                self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": "success"}')
                mock_create.assert_called_once_with(user=self.user, movie=movie_instance, content=self.comment_content)

    def test_personal(self):
        # Mock request object with a user
        request = HttpRequest()
        request.user_ = self.user

        # Call the view function
        response = personal(request)
        print(response.content)

        # Check the response
        self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": {"method_calls": []}}')


class MyCollectTestCase(TestCase):
    def test_mycollect(self):
        # Mock request object with a user
        request = HttpRequest()
        request.user_ = MagicMock()
        request.user_.movie_set.all.return_value = []  # Mock an empty queryset

        # Call the view function
        response = mycollect(request)

        print(response.content)

        # Check the response
        self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": []}')

        request.user_.movie_set.all.assert_called_once()

class MyCommentsTestCase(TestCase):
    def test_my_comments(self):
        # Mock request object with a user
        request = HttpRequest()
        request.user_ = MagicMock()
        request.user_.comment_set.all.return_value = []  # Mock an empty queryset

        # Call the view function
        response = my_comments(request)

        # Check the response
        self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": []}')
        request.user_.comment_set.all.assert_called_once()

class DeleteCommentTestCase(TestCase):
    def test_delete_comment(self):
        # Mock request object with a comment ID
        request = HttpRequest()

        # Mock Comment.objects.get().delete() method
        with patch('movie.models.Comment.objects.get') as mock_get:
            mock_comment = MagicMock()
            mock_get.return_value = mock_comment

            # Call the view function
            response = delete_comment(request, comment_id=1)

            # Check the response
            self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": "success"}')
            mock_comment.delete.assert_called_once()

class MyRateTestCase(TestCase):
    def test_my_rate(self):
        # Mock request object with a user
        request = HttpRequest()
        request.user_ = MagicMock()
        request.user_.rate_set.all.return_value = []  # Mock an empty queryset

        # Call the view function
        response = my_rate(request)

        # Check the response
        self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": []}')
        request.user_.rate_set.all.assert_called_once()

class DeleteRateTestCase(TestCase):
    def test_delete_rate(self):
        # Mock request object with a rate ID
        request = HttpRequest()

        # Mock Rate.objects.filter().delete() method
        with patch('movie.models.Rate.objects.filter') as mock_filter:
            # Call the view function
            response = delete_rate(request, rate_id=1)

            # Check the response
            self.assertEqual(response.content, b'{"Code": 200, "Msg": "\\u6210\\u529f", "Data": "success"}')
            mock_filter.assert_called_once_with(pk=1)
            mock_filter.return_value.delete.assert_called_once()