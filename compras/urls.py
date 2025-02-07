from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_compras, name="get_all_compras"),
    #path('buscar/', views.get_compra_by_date, name="get_compra_by_date"),
    path('create/', views.create_compra, name="create_compra"),
    #path('update/<int:id>/', views.update_compra, name="update_compra"),
    path('delete/<int:id>/', views.delete_compra, name="delete_compra")
]