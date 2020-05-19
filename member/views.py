import json

from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreateForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from .models import Profile
from product.models import Cart
from django.contrib.auth.decorators import login_required
from order.models import OrderList, Order
from product.models import Cart
from django.http import HttpResponse
import json


def signup(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password1']
            password2 = request.POST['password2']
            if password != password2:
                return render(request, 'member/signup.html', {'message': 'password not match'})
            else:
                new_user = User.objects.create_user(username, email, password)
                new_user.save()
                return redirect('/')
        except:
            return render(request, 'member/signup.html', {'message': 'member already existed'})
    else:
        form = UserCreateForm()
    return render(request, 'member/signup.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            request.session['cart_count'] = Cart.objects.filter(
                user_id=request.user.pk).count()
        else:
            return render(request, 'member/login.html', {'message': '아이디와 비밀번호가 일치하지 않습니다.', 'login_form': login_form})
        return redirect('/')
    else:
        login_form = AuthenticationForm()

    return render(request, 'member/login.html', {'login_form': login_form})


def logout(request):
    auth_logout(request)
    return redirect('/')


@login_required(login_url='/member/login/')
def rate(request):
    my_profile = Profile.objects.all()
    orders = Order.objects.filter(user_id=request.user)
    total = sum([order.total_price for order in orders])
    if total > 1000000:
        my_profile.user_grade = 'mvp'
        my_profile.coupon = '30%'
    elif total > 500000:
        my_profile.user_grade = 'platinum'
        my_profile.coupon = '20%'
    else:
        my_profile.user_grade = 'normal'
        my_profile.coupon = '10%'
    context = {
        'total': total,
        'my_profile': my_profile
    }
    return render(request, 'member/profile-rate.html', context)


def service(request):
    return render(
        request,
        'member/service.html/',
        {},
    )


@login_required(login_url='/member/login/')
def service_cancel_list(request):
    return render(
        request,
        'member/service-cancelList.html/',
        {},
    )


@login_required(login_url='/member/login/')
def service_complete(request):
    return render(
        request,
        'member/service-complete.html/',
        {},
    )


@login_required(login_url='/member/login/')
def service_cancel(request):
    my_orders = OrderList.objects.all().order_by('-id')
    context = {
        'my_orders': my_orders
    }
    return render(request, 'member/service-cancel.html/', context)


@login_required(login_url='/member/login/')
def profile(request):
    user_id = request.user

    # user_id에 해당하는 order_id 찾아서 리스트로 만들기
    order_id_list = Order.objects.filter(
        user_id=user_id).values_list('id', flat=True)
    my_orders = OrderList.objects.filter(
        order_id__in=order_id_list).order_by('-id')[:4]
    my_carts = Cart.objects.filter(user_id=user_id).order_by('-id')
    my_profile = Profile.objects.all()
    orders = Order.objects.filter(user_id=user_id)
    total = sum([order.total_price for order in orders])
    if total > 150000:
        my_profile.user_grade = 'mvp'
        my_profile.coupon = '30%'
    elif total > 100000:
        my_profile.user_grade = 'platinum'
        my_profile.coupon = '20%'
    else:
        my_profile.user_grade = 'normal'
        my_profile.coupon = '10%'

    context = {
        'my_orders': my_orders,
        'my_carts': my_carts
    }
    return render(request, 'member/profile.html', context)


@login_required(login_url='/member/login/')
def order(request):
    user_id = request.user

    # user_id에 해당하는 order_id 찾아서 리스트로 만들기
    order_id_list = Order.objects.filter(
        user_id=user_id).values_list('id', flat=True)

    my_orders = OrderList.objects.filter(
        order_id__in=order_id_list).order_by('-id')
    context = {
        'my_orders': my_orders
    }
    return render(request, 'member/profile-orders.html', context)


@login_required(login_url='/member/login/')
def user_info_update(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(
            request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('member:profile')
    else:
        user_change_form = UserChangeForm(instance=request.user)
    return render(request, 'member/profile-update.html', {'user_change_form': user_change_form})


@login_required(login_url='/member/login/')
def user_info_delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('/')
    return render(request, 'member/profile-delete.html')


@login_required(login_url='/member/login/')
def user_info_password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            return redirect('/')
    else:
        password_change_form = PasswordChangeForm(request.user)
    return render(request, 'member/profile-password.html', {'password_change_form': password_change_form})


def change_shipping(request):
    id = int(request.POST['id'])
    receiver = request.POST['receiver']
    phone = request.POST['phone']
    address = request.POST['address']
    memo = request.POST['memo']

    order = OrderList.objects.get(id=id).order_id
    order.receive_name = receiver
    order.receive_phone = phone
    order.receive_address = address
    order.memo = memo
    order.save()

    return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")


def id_find(request):
    email = request.POST['email']
    # template에서 받아온 email과 일치하는 이메일을 갖는 user queryset 반환
    data = User.objects.filter(email=email)

    datas = []

    for dt in data:
        datas.append({'id': dt.username, 'email': dt.email,
                      'date': dt.date_joined, 'name': dt.last_name + dt.first_name})

    # info = {'username':username, 'name':name, 'user_email':user_email, 'date_joined':date_joined }
    return HttpResponse(json.dumps({'info': datas}, indent=4, sort_keys=True, default=str), content_type="application/json")
