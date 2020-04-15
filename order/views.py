from django.contrib.auth.decorators import login_required
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


@login_required
def checkout(request):
    # 세션에서 order_info 가져오기
    order_info = request.session['order_info']

    # order_list 만들기
    order_list = []
    for i in json.loads(order_info['order_list']):
        item = {}
        item['inventory'] = Inventory.objects.get(id=i['inventory-id'])
        item['quantity'] = i['quantity']
        order_list.append(item)

    # 배송지 목록을 불러옴
    shipping_instance = Shipping.objects.all()
    #shipping_instance = get_object_or_404(Shipping)
    if request.method == 'POST':
        ship = Shipping.objects.create(user_id=request.user)
        shipping = ShippingForm(request.POST, instance=ship)
        if shipping.is_valid():
            shipping.save()
            return redirect('order:shipping-show')
    else:
        form = ShippingForm()
    return render(request, 'order/checkout.html', {'order_list': order_list, 'shipping_instance': shipping_instance, "form": form})


class ToCheckout(View):
    def post(self, request):
        # 로그인 안되어있으면 no user 반환
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({'result': 'no user'}), content_type="application/json")

        # 품절 검사
        for i in json.loads(request.POST.get('order-list', False)):
            inventory = Inventory.objects.get(id=i['inventory-id'])
            amount = inventory.amount
            quantity = i['quantity']
            if amount < quantity:
                return HttpResponse(json.dumps(
                    {'result': 'fail', 'message': 'out of stock', 'product': inventory.product_id.name}),
                    content_type="application/json")


        request.session['order_info'] = {}
        request.session['order_info']['is_cart'] = int(
            request.POST.get('is-cart', False))
        request.session['order_info']['order_list'] = request.POST.get(
            'order-list', False)
        request.session['order_info']['amount'] = request.POST.get(
            'amount', False)
        request.session['order_info']['shipping_price'] = request.POST.get(
            'shipping-price', False)
        request.session['order_info']['total_price'] = request.POST.get(
            'total-price', False)
        return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")


class CompleteView(TemplateView):
    template_name = 'order/complete.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        # order를 context에 추가
        order_no = self.kwargs['order_no']
        context['order'] = Order.objects.get(id=order_no)

        # order_list를 context에 추가
        context['order_list'] = OrderList.objects.filter(order_id=order_no)

        return context

class MakeOrder(View):
    def post(self, request):
        # 로그인 안되어있으면 no user 반환
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({'result': 'no user'}), content_type="application/json")

        # 로그인한 유저 정보 가져오기
        user_id = request.user

        # 세션에서 order_info 가져오기
        order_info = self.request.session.pop('order_info', None)

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

        # is_cart 정보
        is_cart = order_info['is_cart']

        # 배송 정보
        receive_address = request.POST.get('receive_name', False)
        receive_name = request.POST.get('receive_phone', False)
        receive_phone = request.POST.get('receive_address', False)
        memo = request.POST.get('memo', False)

        # 결제 금액
        amount = order_info['amount']
        shipping_price = order_info['shipping_price']
        total_price = order_info['total_price']

        # 주문 완료 절차
        # 1. 재고 검사
        # 2. 전 사이즈 재고 하나도 없으면 product 모델에서 품절 표시하기
        # 3. product 모델 판매량 늘리기
        # 4. Order, OrderList 모델 insert
        # => 1번 과정에서 재고 부족으로 exception 발생시 다시 처음 상태로 롤백 시켜야 함(transaction.atomic으로 처리)

        try:
            with transaction.atomic():
                # 1. 재고 검사
                for item in order_list:
                    # 재고 없으면 예외 발생
                    if item['inventory_id'].amount < item['quantity']:
                        # out_of_stock_product = item['product_id'].name
                        raise order.exceptions.OutOfStockError()
                    # 재고 줄이기
                    item['inventory_id'].amount -= item['quantity']
                    item['inventory_id'].save()

                # 2~3. 품절 검사 & 판매량 늘리기
                for item in order_list:
                    # 품절 검사
                    all_inventory = Inventory.objects.filter(product_id=item['product_id'])
                    total_amount = all_inventory.aggregate(total_amount=Sum('amount'))['total_amount']

                    # for inventory in all_inventory:
                    #     if inventory.amount <= 0:
                    #         inventory.soldout = True        # Inventory 모델의 soldout을 True로
                    #         inventory.save()

                    if total_amount <= 0:
                        item['product_id'].soldout = True   # Product 모델의 soldout을 True로

                    # 판매량 늘리기
                    item['product_id'].sales += item['quantity']
                    item['product_id'].save()

                # 4. Order, OrderList 모델 insert
                order_obj = Order(user_id=user_id,
                                  amount=amount,
                                  shipping_price=shipping_price,
                                  total_price=total_price,
                                  receive_address=receive_address,
                                  receive_name=receive_name,
                                  receive_phone=receive_phone,
                                  memo=memo)
                order_obj.save()
                order_no = order_obj.pk

                for item in order_list:
                    order_list_obj = OrderList(order_id=order_obj,
                                               product_id=item['product_id'],
                                               size=item['size'],
                                               quantity=item['quantity'])
                    order_list_obj.save()

                # 장바구니에서 주문했을 시, 장바구니에 담겨있는 상품들 삭제
                if is_cart:
                    data = Cart.objects.filter(user_id=user_id)
                    data.delete()

                return HttpResponse(json.dumps({'result': 'success', 'order_no': order_no}), content_type="application/json")

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
    #shipping_instance = get_object_or_404(Shipping)
    if request.method == 'POST':
        ship = Shipping.objects.create(user_id=request.user)
        shipping = ShippingForm(request.POST, instance=ship)
        if shipping.is_valid():
            shipping.save()
            return redirect('order:shipping-show')
    else:
        form = ShippingForm()
    return render(request, 'order/shipping-show.html', {'shipping_instance': shipping_instance, "form": form})


@login_required
def Shipping_update(request, pk):
    ship = Shipping.objects.get(id=pk)
    pk = ship.pk
    if request.method == 'POST':
        shipping = ShippingForm(request.POST, instance=ship)
        if shipping.is_valid():
            shipping.save()
            return redirect('order:shipping-show')

    else:
        ship = ShippingForm(instance=ship)
    return 


@login_required
def Shipping_delete(request, pk):
    ship = Shipping.objects.get(id=pk)
    if request.method == 'POST':
        ship.delete()
        return redirect('order:shipping-show')
    return render(request, 'order/shipping-delete.html', {'ship':ship})