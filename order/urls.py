
from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('to-checkout1/', views.ToCheckout1.as_view(), name='to-checkout1'),
    path('to-checkout2/', views.ToCheckout2.as_view(), name='to-checkout2'),
    path('complete/', views.CompleteView.as_view(), name='complete'),
    path('make-order/', views.MakeOrder.as_view(), name='make-order'),
    path('checkout/', views.checkout, name='checkout'),
    path('shipping/', views.Shippings, name='shipping'),
    path('shipping-show/', views.ShippingShow, name='shipping-show'),
]
