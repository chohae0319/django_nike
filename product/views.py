from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Category, Product, ProductImage, Inventory


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


def cart(request):
    return render(request, 'product/cart.html', {})


def detail(request):
    return render(request, 'product/detail.html', {})


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/detail.html'

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
