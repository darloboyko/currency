from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def index(request):
    return render(request, 'index.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('currency/', include('currency.urls')),

    path('__debug__/', include('debug_toolbar.urls')),
]
