from django.urls import path
from .views import userLogin, logout_view

urlpatterns = [
    path('login', userLogin, name='login-url'),
    path('logout', logout_view, name='logout-url'),
]