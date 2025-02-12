from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_ingresos, name="get_all_ingresos"),
    path('create_ingreso/<int:cuenta_id>/', views.create_ingreso, name='create_ingreso'),
    path('delete/<int:id>/', views.delete_ingreso, name="delete_ingreso"),
    path('<int:id>/', views.get_ingreso_by_id, name="get_ingreso_by_id")
]