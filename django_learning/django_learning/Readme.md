python3 -m venv venv
source venv/bin/activate

pip install Django
python3 -m pip install Pillow

or 

django-admin startproject project_name
cd project_name

python3 manage.py runserver
python3 manage.py runserver 4000
python3 manage.py runserver 1.2.3.4:4000

python3 manage.py startapp app_name

INSTALLED_APP - add app_name.apps.AppNameConfig
write in views    func_name(request)

from django.urls import path, include, re_path
write in urls path('spec_url/', func_name),
# or path('spec_url/', func_name, name='spec_url'),

re_path(r'^archive/(?P<year>[0-9]{4})/', func_name)

request.GET
request.POST

DEBUG=True
or
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']

404
urls.py
handler404 = pageNotFound

from django.shortcuts import redirect ## default 302, permanent=True - 301

settings.py - DATABASES

from django.db import models

MEDIA_ROOT, MEDIA_URL

python3 manage.py makemigrations
python3 manage.py sqlmigrate news 0001 // for show sql query
python3 manage.py migrate

python3 manage.py shell
from django.db import connection
connection.queries
from django.db import reset_queries
from news.models import News

News.objects.create(...)   or
news1 = News(...)
news1.save()

News.objects.all()
News.objects.filter(title='News 6')
News.objects.get(pk=5) // only one row, (by unique field)

cur_new = News.objects.get(pk=4)
cur_new.title = '...'
cur_new.save()

cur_new.delete()

News.objects.order_by('title')
News.objects.order_by('-title')

News.objects.exclude(title='News 5')

python3 manage.py createsuperuser


news/admin.py
from django.contrib import admin

admin.site.register(ModelName)

# models.py      class Meta
# apps.py   class ModelNameConfig
# admin.py   class ModelNameAdmin(admin.ModelAdmin)

simple_tags
inclusion_tags
templatetags    __init__.py
from django import template
register = template.Library()
@register.simple_tag()
{% load name_tag %}
{% get_categories as categories %}

get_object_or_404(ModelName, pk=post_id)

python3 manage.py collectstatic

News.objects.filter(pk__gt=4, name__contains='title')
News.objects.first()
news1.get_previous_by_created_at()
News.objects.filter(category__title='Политика')

ns = News.objects.all()
ns.update(category_id=4)

Category.objects.filter(news__title__contains='формы').distinct()

from django.db.models import Q
| & ~
News.objects.filter(Q(pk__in=[5, 6]) | Q(title__contains='2'))

News.objects.all()[:3]
News.objects.all()[10:]
News.objects.all()[3:5]

from django.db.models import *

News.objects.aggregate(min_views=Min('vies'), max_views=Max('views'))
News.objects.aggregate(diff=Min('vies')-Max('views'))

// HAVING_BY
cats = Category.objects.annotate(Count('news'))
for item in cats:
    print(item.title, item.news__count)

cats = Category.objects.annotate(max_views=Max('news__views'))

// values
News.objects.values('title','views').get(pk=1)

news = News.objects.values('title','views','category__title')
connection.queries
reset_queries()

// class F
from django.db.models import F

news1 = News.objects.get(pk=1)
news1.views += 1
news1.save()

news1 = News.objects.get(pk=1)
news1.views = F('views') + 1
news1.save()

News.objects.filter(content__icontains=F('title'))

from django.db.models.functions import Length
news = News.objects.annotate(length=Length('title')).all()

// raw
from django.db.models import *
News.objects.raw("SELECT * FROM news_news")
News.objects.raw("SELECT id, title FROM news_news")
News.objects.raw("SELECT id, title FROM news_news WHERE title = %s", ['News 5'])

pip install django-debug-toolbar
pip install django-ckeditor

python3 manage.py collectstatic   !!!!!  на продакшене
STATIC_URL
STATIC_ROOT
STATICFILES_DIRS

pip install django-simple-captcha
