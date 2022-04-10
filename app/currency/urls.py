from currency import views as currency_views

from django.urls import path

app_name = 'currency'


urlpatterns = [
    path('contacts/list/', currency_views.contact_list, name='contact_list'),
    path('rates/list/', currency_views.rate_list, name='rate_list'),
    path('source/list/', currency_views.SourceList.as_view(), name='source_list'),
    path('source/create/', currency_views.SourceCreate.as_view(), name='source_create'),
    path('source/detail/<int:pk>/', currency_views.SourceDetail.as_view(), name='source_detail'),
    path('source/update/<int:pk>/', currency_views.SourceUpdate.as_view(), name='source_update'),
    path('source/delete/<int:pk>/', currency_views.SourceDelete.as_view(), name='source_delete'),
]