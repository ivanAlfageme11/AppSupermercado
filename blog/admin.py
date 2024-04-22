from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


admin.site.register(Supermercados)
admin.site.register(Clientes)
admin.site.register(Ciudades)
admin.site.register(Almacen)
admin.site.register(Productos)
admin.site.register(Productos_almacen)
admin.site.register(Pedidos)
admin.site.register(Productos_pedido)