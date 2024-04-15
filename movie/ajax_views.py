import json
import random
from functools import wraps

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

from movie_it.cache_keys import USER_CACHE, ITEM_CACHE
from movie_it.recommend_movies import recommend_by_user_id, recommend_by_item_id
from .forms import *
from index.utils import success, error


def movies_paginator(movies, page):
    paginator = Paginator(movies, 12)
    if page is None:
        page = 1
    movies = paginator.page(page)
    return movies


# Converts python objects to json type dictionary
def to_dict(l):
    def _todict(obj):
        j = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
        return j

    return [_todict(i) for i in l]


# from django.urls import HT
# json response
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json;"
        super(JSONResponse, self).__init__(content, **kwargs)

def choose_tags(request):
    data = request.json
    # print(data) DEBUG
    tags_name = data.get("tags_name")
    for tag_name in tags_name:
        # create user tag relationship based on user selected tag
        tag = Tags.objects.filter(name=tag_name.strip()).first()
        UserTagPrefer.objects.create(tag_id=tag.id, user_id=request.user_.id, score=5)
    return success()

def login(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')
    result = User.objects.filter(username=username)
    if result:
        user = User.objects.get(username=username)
        if user.password == password:
            return success(data=user.id)
        else:
            return error('Wrong password')
    return error('Account does not exist')


def get_user(request):
    id_ = request.headers.get("access-token")
    user = User.objects.filter(id=id_).first()
    if user:
        return success(
            data={"name": user.username, "role": [],
                  "isSuperuser": True}
        )
    return error()


def register(request):
    data = request.json
    if not all((data.get("username"), data.get("password1"), data.get("password2"))): # if any entry is missing
        return error("Incomplete information")
    if data.get("password1") != data.get("password2"):                                # if two passwords does not match
        return error("inconsistent passwords")
    if User.objects.filter(username=data.get("username")).exists():
        return error("Account already exits")
    user = User.objects.create(
        username=data.get("username"),
        password=data.get("password1"),
        email=data.get("email"))
    # 注册新用户
    return success(data=user.id)


# TODO: not used anywhere C.Ren
# def login_in(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         request = args[0]
#         is_login = request.session.get("login_in")
#         if is_login:
#             return func(*args, **kwargs)
#         else:
#             return redirect(reverse("login"))
#
#     return wrapper


def recent_movies(request):
    new_list = Movie.objects.order_by('?')[:8]
    return success(to_dict(new_list))


def user_recommend(request):
    # cache_key = USER_CACHE.format(user_id=user_id)
    user_id = request.user_.id
    if user_id is None:                                     # if user_id is not provided
        movie_list = Movie.objects.order_by('?')
    else:
        cache_key = USER_CACHE.format(user_id=user_id)
        movie_list = cache.get(cache_key)
        movie_list = recommend_by_user_id(user_id)          # get recommended movies based on user_id
        cache.set(cache_key, movie_list, 60 * 5)

    json_movies = to_dict(movie_list)
    random.shuffle(json_movies)
    return success(json_movies[:3])


def item_recommend(request):
    user_id = request.user_.id
    if user_id is None:
        movie_list = Movie.objects.order_by('?')
    else:
        cache_key = ITEM_CACHE.format(user_id=user_id)
        movie_list = cache.get(cache_key)
        movie_list = recommend_by_item_id(user_id)
        cache.set(cache_key, movie_list, 60 * 5)

    json_movies = to_dict(movie_list)
    random.shuffle(json_movies)
    return success(json_movies[:3])


def movies(request):
    data = request.json
    pagesize = data.get('pagesize', 8)
    page = data.get('page', 1)
    order = data.get('order', 'num')
    tag = data.get('tag')
    if order == 'collect':        # movies are ordered by number of saved times
        movies = Movie.objects.annotate(
            collectors=Count('collect')).order_by('-collectors')
        title = 'Collection sort'
    elif order == 'rate':         # movies are ordered by rating
        movies = Movie.objects.all().annotate(marks=Avg('rate__mark')).order_by('-marks')
        title = 'Rating sort'
    elif order == 'years':        # movies are ordered by released date
        movies = Movie.objects.order_by('-years')
        title = 'Time sort'
    else:                         # movies are ordered by id
        movies = Movie.objects.order_by('-id')
        title = 'Popularity sort'
    if tag:
        movies = movies.filter(tags__id=tag)
    pg = Paginator(movies, pagesize)
    page = pg.page(page)
    return success({
        'total': pg.count,
        'results': to_dict(page.object_list)
    })


def search_movies(request):
    data = request.json
    pagesize = data.get('pagesize', 5)
    page = data.get('page', 1)
    keyword = data.get('keyword', '')
    # match a movie if movie's name/director/leader contains user provided keyword
    q = Q(name__icontains=keyword) | Q(
        director__icontains=keyword) | Q(leader__icontains=keyword)
    movies = Movie.objects.filter(q).order_by('name')
    pg = Paginator(movies, pagesize)
    page = pg.page(page)
    return success(to_dict(page.object_list))


def movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    movie.num += 1
    movie.save()
    result = to_dict([movie])[0]
    result['collect_count'] = movie.collect.count()
    result['image_link'] = str(result['image_link'])
    result['all_tags'] = to_dict(movie.tags.all())
    comments = movie.comment_set.order_by("-create_time")
    for i in comments:
        i.userName = i.user.username
    result['comments'] = to_dict(comments)
    user_id = request.user_.id
    movie_rate = Rate.objects.filter(
        movie=movie).all().aggregate(Avg('mark'))
    if movie_rate:
        movie_rate = movie_rate['mark__avg']
    else:
        movie_rate = 0
    result['movie_rate'] = movie_rate
    if user_id is not None:
        user_rate = Rate.objects.filter(movie=movie, user_id=user_id).first()
        if user_rate:
            result['user_rate'] = to_dict([user_rate])[0]
        else:
            result['user_rate'] = None
        result['user'] = to_dict([request.user_])[0]
        is_collect = movie.collect.filter(id=user_id).first()
        if is_collect:
            result['is_collect'] = to_dict([is_collect])[0]
        else:
            result['is_collect'] = None
    return success(result)


def search(request):
    if request.method == "POST":         # If we are searching page
        key = request.POST["search"]
        request.session["search"] = key
    else:
        key = request.session.get("search")  # Get search keyword
    movies = Movie.objects.filter(
        Q(name__icontains=key) | Q(intro__icontains=key) | Q(
            director__icontains=key)
    )                                        # Fuzzy search
    page_num = request.GET.get("page", 1)
    movies = movies_paginator(movies, page_num)
    return render(request, "items.html", {"movies": movies, 'title': 'Search result'})


def all_tags(request):
    tags = Tags.objects.all()
    return success(to_dict(tags))


# Rate a movie
def score(request, movie_id):
    user_id = request.user_.id
    movie = Movie.objects.get(id=movie_id)
    score = float(request.json.get("score"))
    get, created = Rate.objects.get_or_create(
        user_id=user_id, movie=movie, defaults={"mark": score})
    if created:
        # for this movie's all tags
        for tag in movie.tags.all():
            prefer, created = UserTagPrefer.objects.get_or_create(
                user_id=user_id, tag=tag, defaults={'score': score})
            if not created:
                # we update the current tag score
                prefer.score += (score - 3)
                prefer.save()
        print('create data')
        # clear cache
        user_cache = USER_CACHE.format(user_id=user_id)
        item_cache = ITEM_CACHE.format(user_id=user_id)
        cache.delete(user_cache)
        cache.delete(item_cache)
        print('cache deleted')
    return success()


# Like a movie
def collect(request, movie_id):
    user = request.user_
    movie = Movie.objects.get(id=movie_id)
    movie.collect.add(user)
    movie.save()
    return success()

# Dislike a movie
def decollect(request, movie_id):
    user = request.user_
    movie = Movie.objects.get(id=movie_id)
    movie.collect.remove(user)
    movie.save()
    return success()


def make_comment(request, movie_id):
    user = request.user_
    movie = Movie.objects.get(id=movie_id)
    comment = request.json.get("comment")
    Comment.objects.create(user=user, movie=movie, content=comment)
    return success()


def personal(request):
    user = request.user_
    return success(to_dict([user])[0])

# Return all liked movies
def mycollect(request):
    user = request.user_
    movie = user.movie_set.all()
    for i in movie:
        i.all_tags = to_dict(i.tags.all())
    return success(to_dict(movie))

# Show all my comments
def my_comments(request):
    user = request.user_
    comments = user.comment_set.all()
    for i in comments:
        i.movie_name = i.movie.name
    return success(to_dict(comments))


def delete_comment(request, comment_id):
    Comment.objects.get(pk=comment_id).delete()
    return success()


def my_rate(request):
    user = request.user_
    rate = user.rate_set.all()
    for i in rate:
        i.movie_name = i.movie.name
    return success(to_dict(rate))


def delete_rate(request, rate_id):
    Rate.objects.filter(pk=rate_id).delete()
    return success()

############################################################################################################################################
