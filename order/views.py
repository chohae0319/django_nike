# from django.db.models import Sum, F
# from django.shortcuts import render
# from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, RedirectView
# from .models import Category, Product, ProductImage, Inventory, Cart
# from django.contrib.auth.models import User
# from django.contrib.auth.mixins import LoginRequiredMixin

from product.models import Cart
from django.shortcuts import render
from django.http import HttpResponse
import json

def cart_order(request):
    user_id = request.user.pk

    return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")

def ship_info(request):
    return render(
        request,
        'order/shipinfo_temp.html',
        {}
    )