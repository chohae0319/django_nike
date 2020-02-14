from django.urls import path
from .views import signup, login, logout, home

app_name = 'member'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]