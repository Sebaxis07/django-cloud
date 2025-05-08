from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.transaccion_list_view, name='transaccion_list'),
    path('transacciones/nueva/', views.transaccion_create_view, name='transaccion_create'),
    path('transacciones/<int:pk>/editar/', views.transaccion_update_view, name='transaccion_update'),
    path('transacciones/<int:pk>/eliminar/', views.transaccion_delete_view, name='transaccion_delete'),

    path('categorias/', views.categoria_list_view, name='categoria_list'),
    path('categorias/nueva/', views.categoria_create_view, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update_view, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete_view, name='categoria_delete'),
]