from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signin/', signin_view, name='signup'),
    path('logout', logout_view, name='logout'),
    path('home/', home_view, name='home')
]