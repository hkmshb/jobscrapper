from django.urls import path
from jobs import views


urlpatterns = [
    path('', views.opening_list, name='index'),
    path('o/<int:opening_id>', views.opening_show, name='show')
]
