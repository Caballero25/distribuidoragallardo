from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")),
    path('terceros/', include('terceros.urls')),
    path('productos/', include('productos.urls')),
    path('compras/', include('compras.urls'))
]
