from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Sum
from django.db import transaction
from django.views.generic import TemplateView, View
from product.models import Inventory, Cart
from .models import Order, OrderList, Shipping
from django.http import HttpResponse
import json
import order.exceptions
from .forms import ShippingForm
from django.contrib.auth.decorators import login_required



def checkout(request):
    return render(request, 'order/checkout.html', {})


class ToCheckout1(View):
    def post(self, request, *args, **kwargs):
        request.session['order_info'] = {}
        request.session['order_info']['order_list'] = request.POST.get(
            'order-list', False)
        request.session['order_info']['total_price'] = request.POST.get(
            'total-price', False)
        return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")


class ToCheckout2(View):
    def post(self, request, *args, **kwargs):
        request.session['order_info'] = request.session['order_info']
        request.session['order_info']['receive_name'] = request.POST.get(
            'receive_name', False)
        request.session['order_info']['receive_phone'] = request.POST.get(
            'receive_phone', False)
        request.session['order_info']['receive_address'] = request.POST.get(
            'receive_address', False)
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


class CompleteView(TemplateView):
    template_name = 'order/complete.html'


class MakeOrder(View):
    def post(self, request, *args, **kwargs):
        # 로그인한 유저 정보 가져오기
        user_id = request.user

        # 세션에서 order_info 가져오기
        order_info = self.request.session['order_info']

        # order_list 변환
        order_list = []
        for i in json.loads(order_info['order_list']):
            item = {}
            item['inventory_id'] = Inventory.objects.get(id=i['inventory-id'])
            item['product_id'] = item['inventory_id'].product_id
            item['size'] = item['inventory_id'].size
            item['quantity'] = i['quantity']
            item['is_soldout'] = False
            order_list.append(item)

        # 배송 정보
        receive_address = order_info['receive_address']
        receive_name = order_info['receive_name']
        receive_phone = order_info['receive_phone']

        # 결제 금액
        total_price = order_info['total_price']

        # 주문 완료 절차
        # 1. 재고 검사
        # 2. 계좌 잔액 줄이기(아직 구현 안함)
        # 3. 전 사이즈 재고 하나도 없으면 product 모델에서 품절 표시하기
        # 4. product 모델 판매량 늘리기
        # 5. Order, OrderList 모델 insert
        # => 1,2번 과정에서 재고 부족, 잔액 부족으로 exception 발생시 다시 처음 상태로 롤백 시켜야 함(transaction.atomic으로 처리)

        try:
            with transaction.atomic():
                # 1. 재고 검사
                for item in order_list:
                    # 재고 없으면 예외 발생
                    if item['inventory_id'].amount < item['quantity']:
                        out_of_stock_product = item['product_id'].name
                        raise order.exceptions.OutOfStockError()
                    # 재고 줄이기
                    item['inventory_id'].amount -= item['quantity']
                    item['inventory_id'].save()

                # 2. 계좌 잔액 줄이기(아직 구현 안함)

                # 3~4. 품절 검사 & 판매량 늘리기
                for item in order_list:
                    # 품절 검사
                    all_inventory = Inventory.objects.filter(
                        product_id=item['product_id'])
                    total_amount = all_inventory.aggregate(
                        total_amount=Sum('amount'))['total_amount']
                    if total_amount <= 0:
                        item['product_id'].soldout = True
                    # 판매량 늘리기
                    item['product_id'].sales += item['quantity']
                    item['product_id'].save()

                # 5. Order, OrderList 모델 insert
                order_obj = Order(user_id=user_id,
                                  total_price=total_price,
                                  receive_address=receive_address,
                                  receive_name=receive_name,
                                  receive_phone=receive_phone)
                order_obj.save()

                for item in order_list:
                    order_list_obj = OrderList(order_id=order_obj,
                                               product_id=item['product_id'],
                                               size=item['size'],
                                               quantity=item['quantity'])
                    order_list_obj.save()

                return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")

        # 재고 부족시
        except order.exceptions.OutOfStockError as e:
            return HttpResponse(json.dumps({'result': 'fail', 'message': 'out of stock'}), content_type="application/json")

        # 기타 에러상황
        except Exception as e:
            return HttpResponse(json.dumps({'result': 'fail', 'message': 'unknown error'}), content_type="application/json")


def Shippings(request):
    if request.method == 'POST':
        ship = Shipping.objects.create(user_id=request.user)
        shipping = ShippingForm(request.POST, instance=ship)
        if shipping.is_valid():
            shipping.save()
            return redirect('order:shipping-show')
    else:
        form = ShippingForm()
    return render(request, 'order/shipping.html', {'ship':form})

def ShippingShow(request):
    shipping_instance = Shipping.objects.all()
    return render(request, 'order/shipping-show.html', {'shipping_instance':shipping_instance})


@login_required
def Shipping_update(request, pk):
    ship = Shipping.objects.get(id=pk)
    if request.method == 'POST':
        shipping = ShippingForm(request.POST, instance=ship)
        if shipping.is_valid():
            shipping.save()
            return redirect('order:shipping-show')
    else:
        ship = ShippingForm(instance=ship)
    return render(request, 'order/shipping-update.html', {'ship':ship})

@login_required
def Shipping_delete(request, pk):
    ship = Shipping.objects.get(id=pk)
    if request.method == 'POST':
        ship.delete()
        return redirect('order:shipping-show')
    return render(request, 'order/shipping-delete.html', {'ship':ship})