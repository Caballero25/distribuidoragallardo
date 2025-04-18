from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_compras, name="get_all_compras"),
    path('create/', views.create_compra, name="create_compra"),
    path('delete/<int:id>/', views.delete_compra, name="delete_compra"),
    path('<int:id>/', views.get_compra_by_id, name="get_compra_by_id"),
    path('compra/edit/<str:id>', views.compraUpdateView, name="compra_edit"),
]