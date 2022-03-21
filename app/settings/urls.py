from currency import views as currency_views

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', currency_views.index),
    path('contacts/list/', currency_views.contact_list),
    path('rates/list/', currency_views.rate_list)
]
