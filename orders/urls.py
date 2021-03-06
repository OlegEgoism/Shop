from django.urls import path

from . import views
from .views import getform, celeryhome, getcelery

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('form/', getform, name='form'),
    path('home/', celeryhome, name='home'),
    path('getcelery/', getcelery, name='getcelery'),
]
