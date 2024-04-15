'''
用户对电影的打分数据，以及对电影的评论模型的建立。
'''
from datetime import datetime
from datetime import date
from django.db import models
from django.db.models import Avg
from django.db.models.fields.files import FileField
from itertools import chain
#数据库表
class User(models.Model):
    username = models.CharField(max_length=255, unique=True, verbose_name="account")#unique
    password = models.CharField(max_length=255, verbose_name="password")
    email = models.EmailField(verbose_name="email")
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "FrontUser"
        verbose_name = "FrontUser"

    def __str__(self):
        return self.username


class Tags(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tag", unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tag"

    def __str__(self):
        return self.name


class UserTagPrefer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, verbose_name="Userid",
    )
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, verbose_name='Tags')
    score = models.FloatField(default=0)

    class Meta:
        verbose_name = "UserPreference"
        verbose_name_plural = "Preference"

    def __str__(self):
        return self.user.username + str(self.score)


class Movie(models.Model):
    tags = models.ManyToManyField(Tags, verbose_name='Tag', blank=True)#多对多关系
    collect = models.ManyToManyField(User, verbose_name="Collector", blank=True)
    name = models.CharField(verbose_name="Title", max_length=255, unique=True)
    director = models.CharField(verbose_name="Director Name", max_length=255)
    country = models.CharField(verbose_name="Nation", max_length=255)
    years = models.DateField(verbose_name='Release date')
    leader = models.CharField(verbose_name="Starring", max_length=1024)
    d_rate_nums = models.IntegerField(verbose_name="Rating number")
    d_rate = models.CharField(verbose_name="Rating", max_length=255)
    intro = models.TextField(verbose_name="Description")
    num = models.IntegerField(verbose_name="Browse number", default=0)
    origin_image_link = models.URLField(verbose_name='Image address', max_length=255, null=True)
    image_link = models.FileField(verbose_name="Cover image", max_length=255, upload_to='movie_cover')
    imdb_link = models.URLField(null=True)

    @property
    def movie_rate(self):
        movie_rate = Rate.objects.filter(movie_id=self.id).aggregate(Avg('mark'))['mark__avg']
        return movie_rate or 'None'

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movie"

    def __str__(self):
        return self.name

    def to_dict(self, fields=None, exclude=None):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            if exclude and f.name in exclude:
                continue
            if fields and f.name not in fields:
                continue
            value = f.value_from_object(self)
            if isinstance(value, date):
                value = value.strftime('%Y-%m-%d')
            elif isinstance(f, FileField):
                value = value.url if value else None
            data[f.name] = value
        return data

#用户对电影打分数据
class Rate(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Movieid"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Userid",
    )
    mark = models.FloatField(verbose_name="Rating")
    create_time = models.DateTimeField(verbose_name="Release date", auto_now_add=True)

    @property
    def avg_mark(self):
        average = Rate.objects.all().aggregate(Avg('mark'))['mark__avg']#求平均分
        return average

    class Meta:
        verbose_name = "RatingInfo"
        verbose_name_plural = verbose_name

#电影评论表
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")#外建关联
    content = models.CharField(max_length=255, verbose_name="Content")
    create_time = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = verbose_name


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')

    class Meta:
        verbose_name = "CommentLike"
        verbose_name_plural = verbose_name
