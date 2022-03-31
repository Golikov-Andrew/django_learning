python3 -m venv venv
source venv/bin/activate

pip install Django
django-admin startproject project_name
cd project_name
python3 manage.py runserver
python3 manage.py runserver 4000
python3 manage.py runserver 1.2.3.4:4000

python3 manage.py startapp app_name

python3 manage.py makemigrations
python3 manage.py sqlmigrate news 0001
python3 manage.py migrate

python3 manage.py shell
from django.db import connection
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

class Meta