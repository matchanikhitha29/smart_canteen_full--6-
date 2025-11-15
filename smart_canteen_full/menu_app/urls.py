from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .api_views import items_list, orders_list

urlpatterns = [

    # Home page
    path('', views.home, name='home'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    
    # FIXED LOGOUT
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('register/', views.register_view, name='register'),

    # Menu & Cart
    path('menu/', views.menu_list, name='menu_list'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),

    # Admin Controls
    path('toggle-item/<int:item_id>/', views.toggle_item, name='toggle_item'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Item Management
    path('items/manage/', views.manage_items, name='manage_items'),
    path('items/add/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),

    # APIs
    path('api/items/', items_list, name='api_items'),
    path('api/orders/', orders_list, name='api_orders'),
]
