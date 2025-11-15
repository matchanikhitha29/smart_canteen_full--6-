from django.urls import path
from . import api_views

urlpatterns = [
    path('items/', api_views.items_list, name='api_items'),
    path('orders/', api_views.orders_list, name='api_orders'),
]
