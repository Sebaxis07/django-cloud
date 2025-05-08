from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('tracker.urls', namespace='tracker')),
    path('', lambda request: redirect('tracker:transaccion_list', permanent=True)), # Redirige la raíz a la lista de transacciones
]