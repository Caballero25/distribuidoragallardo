from django.urls import path
from .views import home, obtener_ventas, obtener_compras

urlpatterns = [
    path('', home, name="home-url"),
    path('obtener_ventas/', obtener_ventas, name='obtener_ventas'),
    path('obtener_compras/', obtener_compras, name='obtener_compras'),
]