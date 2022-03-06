from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import manage_items, manage_item, get_state

urlpatterns = [
    path('', manage_items, name='items'),
    path('<slug:key>', manage_item, name='single_item'),
    path('get_state/<str:id>', get_state, name='get_state')

]

urlpatterns = format_suffix_patterns(urlpatterns)
