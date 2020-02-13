from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Category, Product, ProductImage, Inventory

# Create your views here.


# def index(request):
#     return render(
#         request,
#         'product/index.html/',
#         {}
#     )


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

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context(product)를 가져온다.
        context = super(ProductDetail, self).get_context_data(**kwargs)

        # ProductImage를 context에 추가
        context['product_image'] = ProductImage.objects.filter(
            product_id=self.object.pk)

        # Inventory를 context에 추가
        context['inventory'] = Inventory.objects.filter(
            product_id=self.object.pk)

        return context
