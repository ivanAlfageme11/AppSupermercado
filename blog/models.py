from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
    
# Create your models here.

from django.db import models

# Create your models here.
class Ciudades(models.Model):
    codigo_postal=models.IntegerField(primary_key=True)#Max Length 5
    nombre=models.CharField(max_length=30)
    def __str__(self):
        return f"{self.nombre} {self.codigo_postal}"

class Supermercados(models.Model):
    id_supermercado=models.IntegerField(primary_key=True)
    #uuid
    nombre=models.CharField(max_length=70,unique=False)
    ciudad=models.ForeignKey(Ciudades,null=True,blank=True,on_delete=models.SET_NULL)
    def __str__(self):
        return self.nombre

class Clientes(models.Model):
    id_cliente=models.IntegerField(primary_key=True)
    #uuid
    nombre=models.CharField(max_length=20,)
    apellidos=models.CharField(max_length=65,)
    mail=models.EmailField()
    direccion=models.CharField(max_length=50)
    ciudad=models.ForeignKey(Ciudades,null=True,blank=True,on_delete=models.SET_NULL)
    #nombre_supermercado=models.ExpressionList(ListaSupermercados(codigo_postal,File))
    supermercado=models.ForeignKey(Supermercados,null=True,blank=True,on_delete=models.SET_NULL)
    id_user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
class Pedidos(models.Model):
    id_pedido=models.IntegerField(primary_key=True)
    #uuid
    fecha_Pedido=models.DateField()
    fecha_Entrega=models.DateField()
    estado=models.CharField(max_length=15)
    cliente=models.ForeignKey(Clientes,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
    
        return (f"{self.id_pedido} - {self.cliente} /{str(self.fecha_Pedido)} - {str(self.fecha_Entrega)}") 
class Almacen(models.Model):
    id_almacen=models.IntegerField(primary_key=True)
    nombre=models.CharField(max_length=60)
    supermercado=models.ForeignKey(Supermercados,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Productos(models.Model):
    id_Productos=models.IntegerField(primary_key=True)
    #uuid=
    nombre=models.CharField(max_length=60)
    descripcion=models.CharField(max_length=200,null=True,blank=True)
    precioUnitario=models.FloatField()
    stock=models.IntegerField()
    def __str__(self):
        return self.nombre

class Productos_almacen(models.Model):
    id_Producto=models.ForeignKey(Productos,primary_key=True,null=False,blank=True,on_delete=models.CASCADE)
    #uuid
    nombre=models.CharField(max_length=60)
    stock=models.IntegerField()
    almacen=models.ForeignKey(Almacen,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
    
        return (f"{self.nombre}/{self.almacen}")

class Productos_pedido(models.Model):
    #uuid=
    id_producto=models.ForeignKey(Productos,primary_key=True,null=False,blank=True,on_delete=models.CASCADE)
    nombre=models.CharField(max_length=60)
    cantidad=models.IntegerField()
    precio_Total=models.FloatField()
    pedido=models.ForeignKey(Pedidos,null=True,blank=True, on_delete=models.CASCADE)
    def __str__(self):
    
        return (f"{self.nombre}/{self.pedido}")