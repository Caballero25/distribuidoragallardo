from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_cuentas_por_cobrar, name="get_all_cuentas_por_cobrar"),
    path('delete/<int:id>/', views.delete_cuenta_por_cobrar, name="delete_cuenta_por_cobrar"),
    path('<int:id>/', views.get_cuenta_por_cobrar_by_id, name="get_cuenta_por_cobrar_by_id"),
    path('pago/masivo/<str:id>', views.pagoMasivoCuentaPorCobrar, name='pago-masivo-cobro')
]