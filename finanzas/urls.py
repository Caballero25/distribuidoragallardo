from django.urls import path
from .views import ingresos, egresos

urlpatterns = [
    path('ingresos', ingresos, name="registrar-ingresos-url"),
    path('egresos', egresos, name="registrar-egresos-url"),
]