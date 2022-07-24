
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('book_browse.urls')),
    path('library/', include('library.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    
    
 
    
]
""" Порядок URL маршрутов из переменной urlpatterns имеет значение, так как Django читает файл сверху вниз. Следовательно
когда создается запрос на URL-адрес /accounts/signup, 
Django вначале будет искать в django.contrib.auth.urls, и, не найдя такой, перейдет к приложению accounts.urls """
