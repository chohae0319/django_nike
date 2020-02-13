from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, RedirectView
from .models import Category, Product, ProductImage, Inventory

# Create your views here.


def index(request):
    return render(
        request,
        'product/index.html/',
        {}
    )


def product(request):
    return render(request, 'product/product.html', {})


def sign_up(request):
    return render(request, 'product/sign-up.html', {})


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

def add_cart(request):
    return 0