from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_venta, name="create_venta"),
    path('', views.get_all_ventas, name="get_all_ventas"),
    path('delete/<int:id>/', views.delete_venta, name="delete_venta"),
    path('<int:id>/', views.get_venta_by_id, name="get_venta_by_id")
]