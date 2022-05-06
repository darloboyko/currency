from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def index(request):
    return render(request, 'index.html')


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('currency/', include('currency.urls')),

    path('__debug__/', include('debug_toolbar.urls')),
]
