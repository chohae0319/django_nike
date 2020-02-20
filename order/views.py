# from django.db.models import Sum, F
# from django.shortcuts import render
# from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, RedirectView
# from .models import Category, Product, ProductImage, Inventory, Cart
# from django.contrib.auth.models import User
# from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView, View
from product.models import Inventory, Cart
from django.shortcuts import render
from django.http import HttpResponse
import json


class ToCheckout1(View):
    def post(self, request, *args, **kwargs):
        request.session['order_info'] = {}
        request.session['order_info']['order_list'] = request.POST.get('order-list', False)
        request.session['order_info']['total_price'] = request.POST.get('total-price', False)
        return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")


class ToCheckout2(View):
    def post(self, request, *args, **kwargs):
        request.session['order_info'] = request.session['order_info']
        request.session['order_info']['receive_name'] = request.POST.get('receive_name', False)
        request.session['order_info']['receive_phone'] = request.POST.get('receive_phone', False)
        request.session['order_info']['receive_address'] = request.POST.get('receive_address', False)
        request.session['order_info']['memo'] = request.POST.get('memo', False)
        return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")


class Checkout1View(TemplateView):
    template_name = 'order/checkout1_temp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 세션에서 order_info 가져오기
        order_info = self.request.session['order_info']
        
        # order_list context에 추가
        order_list = []
        for i in json.loads(order_info['order_list']):
            item = {}
            item['inventory'] = Inventory.objects.get(id=i['inventory-id'])
            item['quantity'] = i['quantity']
            order_list.append(item)
        context['order_list'] = order_list
        return context

class Checkout2View(TemplateView):
    template_name = 'order/checkout2_temp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 세션에서 order_info 가져오기
        order_info = self.request.session['order_info']

        # order_list context에 추가
        order_list = []
        for i in json.loads(order_info['order_list']):
            item = {}
            item['inventory'] = Inventory.objects.get(id=i['inventory-id'])
            item['quantity'] = i['quantity']
            order_list.append(item)
        context['order_list'] = order_list

        return context