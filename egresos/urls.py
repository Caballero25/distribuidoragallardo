from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_egresos, name="get_all_egresos"),
    path('delete/<int:id>/', views.delete_egreso, name="delete_egreso"),
    path('get_tercero/', views.get_tercero_by_name_din, name="get_tercero_by_name_din"),
]