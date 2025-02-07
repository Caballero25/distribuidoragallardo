from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_cuentas_por_pagar, name="get_all_cuentas_por_pagar"),
    path('delete/<int:id>/', views.delete_cuenta_por_pagar, name="delete_cuenta_por_pagar"),
    path('create_egreso/<int:cuenta_id>/', views.create_egreso, name='create_egreso')
]