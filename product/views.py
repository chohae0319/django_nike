from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Category, Product

# Create your views here.
def index(request):
    return render(
        request,
        'product/index.html/',
        {}
    )
<<<<<<< HEAD

def product_list(request):
    product = Product.objects.all()
    return render(request, 'product/product.html', {'product':product})
=======
>>>>>>> bcc41a2e7bdf2ab2600bad14e7b5ba04b481c7e2
