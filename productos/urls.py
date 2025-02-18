from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_productos, name="get_all_productos"),
    path('create/', views.create_producto, name="create_producto"),
    path('buscar/', views.get_producto_by_name, name="get_producto_by_name"),
    path('update/<int:id>/', views.update_producto, name="update_producto"),
    path('get_producto/', views.get_producto_by_name_din, name="get_producto_by_name_din"),
    path('get_existencia/', views.get_existencia_producto, name="get_existencia_producto"),
    path('get_valor_unitario/', views.get_valor_unitario_producto, name="get_valor_unitario_producto"),
    path('get_codigo/', views.get_codigo_producto, name="get_codigo_producto"),
    path('delete/<int:id>/', views.delete_producto, name="delete_producto"),
    path('validate_nombre/', views.validate_nombre, name='validate_nombre'),
    path('validate_codigo/', views.validate_codigo, name='validate_codigo'),
    path('verificar-nombre/', views.verificar_nombre, name='verificar_nombre'),
    path('verificar-codigo/', views.verificar_codigo, name='verificar_codigo')
]