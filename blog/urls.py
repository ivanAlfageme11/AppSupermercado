from django.contrib import admin
from django.urls import path
from .views import views

urlpatterns = [
    path('login/', views.Login, name='Login'),
    path('auth/',views.auth,name='Auth'),
    path('principal/',views.Principal,name='Principal'),
    path('principal/datos_cliente/',views.datos_cliente,name='datos cliente'),
    path('Hazte_cliente/',views.Pantalla_hacerse_cliente,name='Hazte cliente'),
    path('Hazte_cliente/Supermercados/',views.buscarSupermercado,name='Supermercados'),
    path('principal/Anadir/',views.modalAñadir,name='Añadir'),
    path('principal/Borrar/',views.modalBorrar,name='Borrar'),
    path('principal/Editar/',views.modalEditar,name='Editar'),
    path('principal/AnadirUsuarios/',views.crearUser,name='Crear'),
    path('principal/BorrarUsuarios/',views.borrarUser,name='Eliminar'),
    path('principal/EditarUsuarios/',views.editarUser,name='Editar'),
    path('principal/DatosCompletos/',views.datosCompletos,name='Datos Completos')
]