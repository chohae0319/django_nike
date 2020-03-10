from django.urls import path
# from . import views
from .views import (
    signup,
    login,
    logout,
    profile,
    order,
    user_info_update,
    user_info_delete,
    user_info_password,
    service
)

app_name = 'member'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('order/', order, name='order'),
    path('profile-update/', user_info_update, name='profile-update'),
    path('profile-delete/', user_info_delete, name='profile-delete'),
    path('profile-password/', user_info_password, name='profile-password'),
    path('service/', service, name='service'),
]
