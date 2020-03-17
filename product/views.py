from itertools import chain

from django.db.models import Sum, F
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, RedirectView
from .models import Category, Product, ProductImage, Inventory, Cart
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, request, JsonResponse
from django.utils import timezone
import member.urls
import datetime
from django.core import serializers
import json
import itertools


# def index(request):
#     return render(
#         request,
#         'product/index.html/',
#     )

def index(request):
    # 각 카테고리에서 판매량 1순위인 상품 리스트에 추가
    # MEN, WOMEN 구분 함.
    product_list = []
    category = Category.objects.all()
    count = range(1, len(category)+1)
    pro3 = Product.objects.filter(gender__isnull=True)
    for i in count:
        # pro: men의 category_id가 i인 상품 중 판매량 1순위인 상품 1개
        # pro2: women의 category_id가 i인 상품 중 판매량 1순위인 상품 1개
        # pro3: men과 women의 각 카테고리에서 판매량 1순위인 상품 최종 리스트
        pro = Product.objects.filter(gender='MEN', category_id=i).order_by('-sales')[:1]
        pro2 = Product.objects.filter(gender='WOMEN', category_id=i).order_by('-sales')[:1]
        pro3 = itertools.chain(pro, pro2, pro3)
    product_list = pro3
    return render(
        request,
        'product/index.html/',
        {'product_list': product_list},
    )


def about(request):
    return render(
        request,
        'product/about.html/',
        {},
    )


def error(request):
    return render(
        request,
        'product/error.html/',
        {},
    )


def FilterDetail(request):
    template_name = 'product/product.html'
    if request.method == "POST":
        size_list = request.POST.getlist('size')
        align = request.POST.get('orderType')
        url = request.POST.get('url')
        url = url.split('/')[3:5]

        size_id = []
        for i in size_list:
            product = Inventory.objects.filter(size=i, soldout=False).values_list('product_id', flat=True)
            for pro in product:
                size_id.append(pro)

        # 사이즈 필터 선택 유무 flag
        if not size_id:
            size_flag = 0
        else:
            size_flag = 1

        # 정렬 방식 선택 유무 flag
        if align is None:
            align_flag = 0
        else:
            align_flag = 1

        if url[0] == '1':
            # MEN 카테고리
            gender = 'Men'
            if url[1] == '0':
                # 신발 전체
                if size_flag == 1:
                    # 사이즈 필터 ON
                    if align_flag == 1:
                        # 정렬 방식 선택(align: 정렬 방식)
                        queryset = Product.objects.filter(gender='MEN', pk__in=size_id)
                        product_list = serializers.serialize("json", FilterList(align, queryset))
                    else:
                        product_list = serializers.serialize("json",
                                                             Product.objects.filter(gender='MEN', pk__in=size_id))
                else:
                    # 사이즈 필터 OFF
                    if align_flag == 1:
                        # 정렬 방식 선택(align: 정렬 방식)
                        queryset = Product.objects.filter(gender='MEN')
                        product_list = serializers.serialize("json", FilterList(align, queryset))
                    else:
                        product_list = serializers.serialize("json", Product.objects.filter(gender='MEN'))
                category = '신발'
            else:
                # 카테고리 별 신발
                if size_flag == 1:
                    if align_flag == 1:
                        queryset = Product.objects.filter(gender='MEN', category_id=url[1], pk__in=size_id)
                        product_list = serializers.serialize("json", FilterList(align, queryset))
                    else:
                        product_list = serializers.serialize("json",
                                                             Product.objects.filter(gender='MEN', category_id=url[1],
                                                                                    pk__in=size_id))
                else:
                    if align_flag == 1:
                        queryset = Product.objects.filter(gender='MEN', category_id=url[1])
                        product_list = serializers.serialize("json", FilterList(align, queryset))
                    else:
                        product_list = serializers.serialize("json", Product.objects.filter(gender='MEN', category_id=url[1]))
                category = serializers.serialize("json", Category.objects.filter(pk=url[1]), fields=('name'))
        else:
            # WOMEN 카테고리
            gender = 'Women'
            if url[1] == '0':
                # 신발 전체
                if size_flag == 1:
                    # 사이즈 필터 ON
                    if align_flag == 1:
                        # 정렬 방식 선택(align: 정렬 방식)
                        queryset = Product.objects.filter(gender='WOMEN', pk__in=size_id)
                        product_list = serializers.serialize("json", FilterList(align, queryset))
                    else:
                        product_list = serializers.serialize("json",
                                                             Product.objects.filter(gender='WOMEN', pk__in=size_id))
                else:
                    # 사이즈 필터 OFF
                    if align_flag == 1:
                        queryset = Product.objects.filter(gender='WOMEN')
                        product_list = serializers.serialize("json", FilterList(align, queryset))
                    else:
                        product_list = serializers.serialize("json", Product.objects.filter(gender='WOMEN'))
                category = '신발'
            else:
                # 카테고리 별 신발
                if size_flag == 1:
                    if align_flag == 1:
                        queryset = Product.objects.filter(gender='WOMEN', category_id=url[1], pk__in=size_id)
                        product_list = serializers.serialize("json", FilterList(align, queryset))
                    else:
                        product_list = serializers.serialize("json",
                                                             Product.objects.filter(gender='WOMEN', category_id=url[1],
                                                                                    pk__in=size_id))
                else:
                    if align_flag == 1:
                        queryset = Product.objects.filter(gender='WOMEN', category_id=url[1])
                        product_list = serializers.serialize("json", FilterList(align, queryset))
                    else:
                        product_list = serializers.serialize("json",
                                                             Product.objects.filter(gender='WOMEN', category_id=url[1]))
                category = serializers.serialize("json", Category.objects.filter(pk=url[1]), fields=('name'))

        ret = {'product_list': product_list,
               'gender': gender,
               'category': category}

        return HttpResponse(json.dumps(ret), content_type='application/json')


def FilterList(align, queryset):
    # 선택 된 정렬 방식에 따라 상품 align

    if align == '신상품순':
        product_list = queryset.order_by('-release_date')
    elif align == '낮은 가격순':
        product_list = queryset.order_by('price')
    else:
        product_list = queryset.order_by('-price')

    return product_list


class CategoryDetail(ListView):
    model = Product
    template_name = 'product/product.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        gender = self.kwargs['gender']
        id = self.kwargs['id']
        if gender == 1:
            context['gender'] = 'Men'
            if id == 0:
                context['product_list'] = Product.objects.filter(gender='MEN')
                context['category'] = '신발'
            else:
                context['product_list'] = Product.objects.filter(gender='MEN', category_id=id)
                context['category'] = Category.objects.filter(pk=id).values('name')
        else:
            context['gender'] = 'Women'
            if id == 0:
                context['product_list'] = Product.objects.filter(gender='WOMEN')
                context['category'] = '신발'
            else:
                context['product_list'] = Product.objects.filter(gender='WOMEN', category_id=id)
                context['category'] = Category.objects.filter(pk=id).values('name')

        return context


class NewProductList(ListView):
    # 모든 신발 카테고리 해당. today 기준 출시일이 30일 전 이내인 상품만
    model = Product
    template_name = 'product/product.html'

    def get_context_data(self, **kwargs):
        context = super(NewProductList, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']

        date_format = "%Y-%m-%d"
        one_month_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime(date_format)
        now_date = datetime.datetime.now().strftime(date_format)

        if pk == 1:
            context['product_list'] = Product.objects.filter(
                gender='MEN',
                release_date__range=[one_month_ago, now_date]
            ).reverse()
        else:
            context['product_list'] = Product.objects.filter(
                gender='WOMEN',
                release_date__range=[one_month_ago, now_date]
            ).reverse()

        return context


class BestProductList(ListView):
    model = Product
    template_name = 'product/best.html'

    def get_context_data(self, **kwargs):
        context = super(BestProductList, self).get_context_data(**kwargs)
        # 판매량 내림차순으로 상위 5개 상품 출력.
        # 카테고리마다 구별해서 템플릿 표시.
        pk = self.kwargs['pk']
        if pk == 1:
            # MEN의 BEST 품목
            context['life_product_list'] = Product.objects.filter(gender='MEN', category_id=1).order_by('-sales')[:5]
            context['run_product_list'] = Product.objects.filter(gender='MEN', category_id=2).order_by('-sales')[:5]
            context['bask_product_list'] = Product.objects.filter(gender='MEN', category_id=3).order_by('-sales')[:5]
            context['soc_product_list'] = Product.objects.filter(gender='MEN', category_id=4).order_by('-sales')[:5]
            context['flip_product_list'] = Product.objects.filter(gender='MEN', category_id=5).order_by('-sales')[:5]
            context['gender'] = 1
        else:
            # WOMEN의 BEST 품목
            context['life_product_list'] = Product.objects.filter(gender='WOMEN', category_id=1).order_by('-sales')[:5]
            context['run_product_list'] = Product.objects.filter(gender='WOMEN', category_id=2).order_by('-sales')[:5]
            context['bask_product_list'] = Product.objects.filter(gender='WOMEN', category_id=3).order_by('-sales')[:5]
            context['soc_product_list'] = Product.objects.filter(gender='WOMEN', category_id=4).order_by('-sales')[:5]
            context['flip_product_list'] = Product.objects.filter(gender='WOMEN', category_id=5).order_by('-sales')[:5]
            context['gender'] = 2
        return context


class SaleProductList(ListView):
    model = Product
    template_name = 'product/product-sales.html'

    def get_context_data(self, **kwargs):
        context = super(SaleProductList, self).get_context_data(**kwargs)
        id = self.kwargs['id']
        gender = self.kwargs['gender']

        date_format = "%Y-%m-%d"
        three_month_ago = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime(date_format)
        now_date = datetime.datetime.now().strftime(date_format)

        url = []
        category = []

        # 카테고리 별 url & 카테고리 name 리스트
        for i in range(1, 6):
            category_id = Category.objects.filter(pk=i).values_list('name', flat=True)
            for k in category_id:
                category.append(k)
            for j in range(1, 3):
                url.append("{% url 'products:sale' " + str(j) + ' ' + str(i) + " %}")
        context['url'] = url
        context['category'] = category

        # 카테고리 별 sale 상품 리스트
        if gender == 1:
            if id == 0:
                context['product_list'] = Product.objects.filter(
                    gender='MEN',
                    release_date__lte=three_month_ago,
                    soldout=False
                )
            else:
                context['product_list'] = Product.objects.filter(
                    gender='MEN',
                    release_date__lt=three_month_ago,
                    soldout=False,
                    category_id=id
                ).reverse()
        else:
            if id == 0:
                context['product_list'] = Product.objects.filter(
                    gender='WOMEN',
                    release_date__lt=three_month_ago,
                    soldout=False
                ).reverse()
            else:
                context['product_list'] = Product.objects.filter(
                    gender='WOMEN',
                    release_date__lt=three_month_ago,
                    soldout=False,
                    category_id=id
                ).reverse()

        return context


# def cart(request):
#     return render(request, 'product/cart.html', {})


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
        context['category'] = Category.objects.get(
            pk=self.object.category_id.pk)

        # ProductImage를 context에 추가
        context['product_image'] = ProductImage.objects.filter(
            product_id=self.object.pk)

        # Inventory를 context에 추가
        context['inventory'] = Inventory.objects.filter(
            product_id=self.object.pk)
        return context


def add_cart(request):      # 장바구니에 상품 추가
    # 로그인 안되어있으면 no user 반환
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps({'result': 'no user'}), content_type="application/json")

    user_id = request.user.pk
    inventory_id = request.POST['inventory']
    quantity = int(request.POST['quantity'])
    all_cart = Cart.objects.filter(user_id=user_id)
    try:
        exist_cart = all_cart.get(inventory_id=inventory_id)
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

    request.session['cart_count'] = all_cart.count()

    return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")


def cart_delete_one(request):      # 장바구니 특정상품 삭제
    # 로그인 안되어있으면 no user 반환
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps({'result': 'no user'}), content_type="application/json")

    user_id = request.user.pk
    cart_id = request.POST['cart-id']
    data = Cart.objects.get(id=cart_id)     # id가 cart_id와 일치하는 쿼리셋 반환

    # 삭제 성공
    data.delete()
    request.session['cart_count'] -= 1
    return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")


def cart_delete_all(request):      # 장바구니 전체상품 삭제
    # 로그인 안되어있으면 no user 반환
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps({'result': 'no user'}), content_type="application/json")

    user_id = request.user.pk

    data = Cart.objects.filter(user_id=user_id)     # user_id가 일치하는 쿼리셋 반환
    data.delete()

    request.session.pop('cart_count', None)

    return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")


def get_option(request, **kwargs):
    # inventory id 가져오기
    product_id = kwargs['pk']
    inventory_set = Inventory.objects.filter(product_id=product_id)
    product = Product.objects.get(id=product_id)
    product_image = ProductImage.objects.filter(product_id=product_id)

    name = product.name
    category = product.category_name()
    price = product.price
    image = []
    inventory = []
    image.append(product.thumbnail.url)
    for i in product_image:
        image.append(i.image.url)
    for i in inventory_set:
        inventory.append({'id': i.id, 'size': i.size, 'amount': i.amount})

    option = {'name': name, 'category': category, 'price': price, 'image': image, 'inventory': inventory}

    return HttpResponse(json.dumps({'result': 'success', 'option': option}), content_type="application/json")


def change_option(request):
    cart_id = request.POST['cart-id']
    inventory_id = request.POST['inventory-id']

    cart = Cart.objects.get(pk=cart_id)
    cart.inventory_id = Inventory.objects.get(pk=inventory_id)
    cart.save()

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

            # 배송비(5만원 이상 무료배송)
            if context['amount'] >= 50000:
                context['shipping_price'] = 0
            else:
                context['shipping_price'] = 2500

            #총 결제 예정 금액
            context['total_price'] = context['amount'] + context['shipping_price']

        return context
