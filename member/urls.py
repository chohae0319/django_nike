from django.urls import path
# from . import views
from .views import signup, login, logout, profile

app_name = 'member'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]
