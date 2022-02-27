from django.urls import path
from . import views
from .views import getform

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('form/', getform, name='form'),
]