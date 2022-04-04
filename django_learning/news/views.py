from re import template
from unicodedata import category
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, News
from .forms import NewsForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'hello world'
    # queryset = News.objects.select_related('category')
    # extra_context = {
    #     'title':'main'
    # }

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
