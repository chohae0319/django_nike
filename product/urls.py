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
#    path('product/', views.product, name='product'),
    path('product/<int:pk>', views.CategoryDetail.as_view(), name='list'),
    path('product/best/<int:pk>', views.BestProductList.as_view(), name='best'),
    path('cart/', views.cart, name='cart'),
    path('product/detail/<int:pk>/', views.ProductDetail.as_view(), name='detail'),
]
