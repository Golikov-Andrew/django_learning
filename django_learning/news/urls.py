from django.urls import path, re_path
from .views import *
# from django.views.decorators.cache import cache_page


urlpatterns = [
    path('register/', register, name='register'),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # path('', index, name='home'),
    path('contacts/', contacts, name='contacts'),
    # path('', cache_page(60)(HomeNews.as_view()), name='home'),
    path('', HomeNews.as_view(), name='home'),
    # path('category/<int:category_id>/', get_category, name='category'),
    path('category/<int:category_id>/', NewsByCategory.as_view(extra_context={
        'title':'Тайтл'
    }), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
]