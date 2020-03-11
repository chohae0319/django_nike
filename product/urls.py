"""nike_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.index),
    path('product/about',views.about, name='about'),
    path('product/error',views.error,name='error'),
    path('product/all/<int:gender>/<int:id>', views.CategoryDetail.as_view(), name='list'),
    path('product/size/', views.SizeDetail, name='size'),
    path('product/new/<int:pk>', views.NewProductList.as_view(), name='new'),
    path('product/best/<int:pk>', views.BestProductList.as_view(), name='best'),
    path('product/sale/<int:pk>', views.SaleProductList.as_view(), name='sale'),
    # 데이터 전송 없는 읽기전용 페이지 입니다.
    path('cart/', views.CartList.as_view(), name='cart'),
    path('product/detail/<int:pk>/', views.ProductDetail.as_view(), name='detail'),
    path('cart/add/', views.add_cart, name='add-cart'),
    path('cart/delete-one/', views.cart_delete_one, name='cart-delete-one'),
    path('cart/delete-all/', views.cart_delete_all, name='cart-delete-all'),
    path('cart/get-option/<int:pk>/', views.get_option, name='get-option'),
]
