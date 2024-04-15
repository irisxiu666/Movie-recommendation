"""movierecomend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from movie import ajax_views as views
# Connecting front and backend
# url patterns contains mappings from url to Django views.
urlpatterns = [
    path("", include("index.urls")),
    path("admin/", admin.site.urls),
    path("api/", include([
        path("login/", views.login, name="login"),                          # Includes all URLs defined in 'index.urls'
        path("register/", views.register, name="register"),                 # configures url routes for Django built-in admin interface
        path("user/", views.get_user, name="get_user"),
        path("recent_movies/", views.recent_movies),
        path("movies/", views.movies),
        path("search_movies/", views.search_movies),
        path("user_recommend/", views.user_recommend,
             name="user_recommend"),                                        # recommendation based on the user
        path("all_tags/", views.all_tags, name="all_tags"),
        path("movie/<int:movie_id>/", views.movie, name="movie"),
        path("item_recommend/", views.item_recommend,
             name="item_recommend"),                                        # recommendation based on the item
        path("score/<int:movie_id>/", views.score, name="score"),           # Give a score to a movie with movie_id
        path("collect/<int:movie_id>/", views.collect, name="collect"),     # Save a movie as favorite
        path("decollect/<int:movie_id>/", views.decollect, name="decollect"), # Deselect a movie as favorite
        path("comment/<int:movie_id>/", views.make_comment, name="comment"),  # Add a comment to a movie
        path("personal/", views.personal),
        path("mycollect/", views.mycollect, name="mycollect"),                # Get all saved favorite movie
        path("my_comments/", views.my_comments, name="my_comments"),          # Get all my comments
        path("my_rate/", views.my_rate, name="my_rate"),                      # Get all my ratings
        path("delete_comment/<int:comment_id>",
             views.delete_comment, name="delete_comment"),
        path("delete_rate/<int:rate_id>", views.delete_rate, name="delete_rate"),
        path('choose_tags/', views.choose_tags)
    ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

admin.site.site_header = 'Recommendation Backend'
admin.site.index_title = 'Home-Recommendation System'
admin.site.site_title = 'Recommendation System'
