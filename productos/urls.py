from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_productos, name="get_all_productos"),
    path('buscar/', views.get_producto_by_name, name="get_producto_by_name"),
    path('update/<int:id>/', views.update_producto, name="update_producto"),
    path('delete/<int:id>/', views.delete_producto, name="delete_producto"),
]