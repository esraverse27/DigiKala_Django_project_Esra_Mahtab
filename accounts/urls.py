from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signin/', signup, name='signup'),
    path('logout', logout_view, name='logout'),
]
