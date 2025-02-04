from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_terceros, name="get_all_terceros"),
    path('<int:id>/', views.get_tercero_by_id, name="get_tercero_by_id"),
    path('buscar/', views.get_tercero_by_name, name="get_tercero_by_name"),
    path('create/', views.create_tercero, name="create_tercero"),
    path('update/<int:id>/', views.update_tercero, name="update_tercero"),
    path('delete/<int:id>/', views.delete_tercero, name="delete_tercero"),
]