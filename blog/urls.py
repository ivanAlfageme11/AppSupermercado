from django.contrib import admin
from django.urls import path
from .views import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'Usuarios', views.UserViewset,basename='MyModel')
router.register(r'Ciudades', views.CiudadesViewset)
router.register(r'Supers', views.SupersViewset)
router.register(r'Clientes', views.ClientesViewset)
router.register(r'Pedidos', views.PedidosViewset)


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
    path('principal/DatosCompletos/',views.datosCompletos,name='Datos Completos'),
    path('principal/Exportar/',views.crearExcel,name='Excel'),
    path('usuarios/Editar', views.Editar_Usuario_API.as_view()),
    path('usuarios/', views.user_list.as_view()),
    path('usuarios/<int:pk>/', views.user_Detail.as_view()),
    path('api/',include(router.urls),name='blog'),
]