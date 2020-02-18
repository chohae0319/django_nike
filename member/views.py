from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from .models import Profile, Order


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
        else:
            return render(request, 'member/login.html', {'message': 'password not match'})
        return redirect('/')
    else:
        login_form = AuthenticationForm()

    return render(request, 'member/login.html', {'login_form': login_form})


def logout(request):
    auth_logout(request)
    return redirect('/')


def profile(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    context = {
        'my_orders': my_orders
    }
    return render(request, 'member/profile.html', {})


def order(request):
    return render(request, 'member/profile-orders.html', {})

# 기존에 있던 profile_view 파일 삭제