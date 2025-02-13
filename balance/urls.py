from django.urls import path
from .views import balance

urlpatterns = [
    path('', balance, name="balance-url"),
]