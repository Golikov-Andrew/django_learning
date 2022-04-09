import os
from re import template
from unicodedata import category
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

# from ..django_learning.settings import EMAIL_HOST_USER
from .models import Category, News
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth import login, logout
# from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages


def contacts(request):
    # objects = ['john1', 'paul2', 'george3', 'ringo4',
    # 'john5', 'paul6', 'george7', 'ringo8','john9', 'paul10', 'george11', 'ringo12']
    # paginator = Paginator(objects, 2)
    # page_num = request.GET.get('page',1)
    # page_objects = paginator.get_page(page_num)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            result = send_mail(
                cleaned_data['subject'],
                cleaned_data['content'],
                str(os.getenv('EMAIL_HOST_USER')),
                ['andrejgolikov46@gmail.com'],
                fail_silently=False
            )
            if result == 1:
                messages.success(request, 'Письмо отправлено')
                return redirect('contacts')
            else:
                messages.error(request, 'Письмо не отправлено')

        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()

    return render(request, 'news/test.html', {'form': form})


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'hello world'
    # queryset = News.objects.select_related('category')
    # extra_context = {
    #     'title':'main'
    # }
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news':news,
#         'title':'News List'
#         }
#     return render(request,'news/index.html', context)


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    mixin_prop = 'hello world'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news':news,
#         'title':category.title,
#         'category':category,
#         }
#     return render(request,'news/category.html', context)


# def view_news(request, news_id):
#     # news_item = News.objects.get_object_or_404(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request,'news/view_news.html', {
#         'news_item':news_item
#     })


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)

#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html' , {
#         'form':form
#     })


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # login_url = '/admin/'
    raise_exception = True
    # success_url = reverse_lazy('home')


def register(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            # return redirect('home')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')

    else:
        # form = UserCreationForm()
        form = UserRegisterForm()
    #     return render(request, 'news/add_news.html' , {
    #     'form':form
    #     })
    # form = UserCreationForm()
    return render(request, 'news/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page Not Found</h1>')

def archive(request, year):
    if int(year) > 2020:
        raise Http404()
    return HttpResponse(f"<h1>Archive</h1><p>{year}</p>")