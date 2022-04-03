from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, News
from .forms import NewsForm
from django.views.generic import ListView


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # extra_context = {
    #     'title':'main'
    # }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news':news, 
#         'title':'News List'
#         }
#     return render(request,'news/index.html', context)


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    context = {
        'news':news, 
        'title':category.title,
        'category':category,
        }
    return render(request,'news/category.html', context)


def view_news(request, news_id):
    # news_item = News.objects.get_object_or_404(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request,'news/view_news.html', {
        'news_item':news_item
    })


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # news = News.objects.create(**form.cleaned_data)
            news = form.save()
            return redirect(news)

    else:
        form = NewsForm()
    return render(request, 'news/add_news.html' , {
        'form':form
    })
