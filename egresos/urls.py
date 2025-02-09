from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_egresos, name="get_all_egresos"),
    path('create_egreso/<int:cuenta_id>/', views.create_egreso, name='create_egreso'),
    path('delete/<int:id>/', views.delete_egreso, name="delete_egreso")
]