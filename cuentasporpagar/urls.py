from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_cuentas_por_pagar, name="get_all_cuentas_por_pagar"),
    path('delete/<int:id>/', views.delete_cuenta_por_pagar, name="delete_cuenta_por_pagar"),
    path('<int:id>/', views.get_cuenta_por_pagar_by_id, name="get_cuenta_por_pagar_by_id")
]