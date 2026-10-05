from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('menu/', views.menu_list, name='menu_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('cart/add/food/<int:food_id>/', views.food_add_to_cart, name='food_add_to_cart'),
    path('cart/add/room/<int:room_id>/', views.room_add_to_cart, name='room_add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
]