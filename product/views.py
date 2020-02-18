from django.db.models import Sum, F
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, RedirectView
from .models import Category, Product, ProductImage, Inventory, Cart
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

import json


def index(request):
    return render(
        request,
        'product/index.html/',
        {}
    )


class CategoryDetail(DetailView):
    model = Product
    template_name = 'product/product.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['product_list'] = Product.objects.filter(category_id=self.object.pk)

        return context


class BestProductList(DetailView):
    model = Product
    template_name = 'product/best.html'
    # context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        context = super(BestProductList, self).get_context_data(**kwargs)
        # 판매량 내림차순으로 상위 1개 상품 출력.
        pk = self.kwargs['pk']
        if pk == 1:
            category_list = Category.objects.filter(main_class='MEN').values('pk')
            productlist = []
            for id in range(len(category_list)):
                categoryid = category_list[id]['pk']
                productlist.append(Product.objects.filter(category_id=categoryid).order_by('-sales')[:1])
                context['product_list'] = productlist

        return context


def cart(request):
    return render(request, 'product/cart.html', {})
  
def detail(request):
    return render(request, 'product/detail.html', {})


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'   # object name을 product로
    template_name = 'product/detail.html'   # 연결 템플릿을 detail.html로 지정

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context(product)를 가져온다.
        context = super(ProductDetail, self).get_context_data(**kwargs)

        # Category를 context에 추가
        context['category'] = Category.objects.get(pk=self.object.category_id.pk)

        # ProductImage를 context에 추가
        context['product_image'] = ProductImage.objects.filter(product_id=self.object.pk)

        # Inventory를 context에 추가
        context['inventory'] = Inventory.objects.filter(product_id=self.object.pk)
        return context


def add_cart(request):      # 장바구니에 상품 추가
    # 로그인 안되어있으면 no user 반환
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps({'result': 'no user'}), content_type="application/json")

    user_id = request.user.pk
    inventory_id = request.POST['inventory']
    quantity = int(request.POST['quantity'])
    try:
        exist_cart = Cart.objects.filter(user_id=user_id).get(inventory_id=inventory_id)
        if exist_cart is not None:      # 장바구니에 동일 상품이 존재할 때, quantity만 늘려줌
            exist_cart.quantity += quantity
            exist_cart.save()
        else:       # 장바구니에 새로 추가
            cart_instance = Cart(user_id=User.objects.get(id=user_id),
                                 inventory_id=Inventory.objects.get(id=inventory_id), quantity=quantity)
            cart_instance.save()
    except Cart.DoesNotExist:        # 유저가 장바구니에 담은 게 하나도 없을 때
        cart_instance = Cart(user_id=User.objects.get(id=user_id), inventory_id=Inventory.objects.get(id=inventory_id),
                             quantity=quantity)
        cart_instance.save()

    return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")


def cart_delete_one(request):      # 장바구니 특정상품 삭제
    # 로그인 안되어있으면 no user 반환
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps({'result': 'no user'}), content_type="application/json")

    user_id = request.user.pk
    cart_id = request.POST['cart-id']
    data = Cart.objects.get(id=cart_id)     # id가 cart_id와 일치하는 쿼리셋 반환

    if data.user_id.id == user_id:       # 삭제 성공
        data.delete()
        return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")
    else:       # Cart의 user_id와 로그인한 유저가 다른 경우
        return HttpResponse(json.dumps({'result': 'no action'}), content_type="application/json")


def cart_delete_all(request):      # 장바구니 전체상품 삭제
    # 로그인 안되어있으면 no user 반환
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps({'result': 'no user'}), content_type="application/json")

    user_id = request.user.pk

    # Cart의 user_id와 로그인한 유저가 다른 경우
    if int(request.POST['user-id']) != user_id:
        return HttpResponse(json.dumps({'result': 'no action'}), content_type="application/json")

    data = Cart.objects.filter(user_id=user_id)     # user_id가 일치하는 쿼리셋 반환
    data.delete()
    return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")


class CartList(LoginRequiredMixin, ListView):
    login_url = '/member/login/'

    context_object_name = 'cart'  # object name을 cart로
    template_name = 'product/cart.html'  # 연결 템플릿을 cart.html로 지정

    def get_queryset(self):
        return Cart.objects.filter(user_id=self.request.user)

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context(product)를 가져온다.
        context = super(CartList, self).get_context_data(**kwargs)
        queryset = self.get_queryset()

        if queryset.count() == 0:
            # 장바구니에 상품이 없는 경우
            context['total_quantity'] = 0
            context['amount'] = 0
        else:
            # 장바구니 상품 개수
            queryset1 = queryset.aggregate(total_quantity=Sum('quantity'))
            context['total_quantity'] = queryset1['total_quantity']

            # 장바구니 상품 금액
            queryset2 = queryset.annotate(price_sum=F('inventory_id__product_id__price')*F('quantity'))\
                .aggregate(amount=Sum('price_sum'))
            context['amount'] = queryset2['amount']

        return context