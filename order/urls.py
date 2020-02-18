
from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('cart-order/', views.cart_order, name='cart-order'),
    path('ship-info/', views.ship_info, name='ship-info'),
    # path('product/<int:pk>', views.CategoryDetail.as_view(), name='list'),
    # path('cart/', views.CartList.as_view(), name='cart'),
    # path('product/detail/<int:pk>/', views.ProductDetail.as_view(), name='detail'),
    # path('cart/add/', views.add_cart, name='add-cart'),
    # path('cart/delete-one/', views.cart_delete_one, name='cart-delete-one'),
    # path('cart/delete-all/', views.cart_delete_all, name='cart-delete-all'),
]
