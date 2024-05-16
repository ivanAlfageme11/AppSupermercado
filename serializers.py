from rest_framework import serializers,generics
from django.contrib.auth.models import User
from blog.views.views import Ciudades,Supermercados,Clientes,Pedidos
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name','last_name', 'email','password','is_staff']

class CiudadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudades
        fields=['codigo_postal','nombre']
class CiudadesList(generics.ListAPIView):
    queryset=Ciudades.objects.all()
    serializer_class=CiudadesSerializer

class SuperSerializer(serializers.ModelSerializer):
    class Meta:
        model= Supermercados
        fields=['id_supermercado','nombre','ciudad_id']
class SuperList(generics.ListAPIView):
    queryset=Supermercados.objects.all()
    serializer_class=SuperSerializer

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Clientes
        fields=['id_cliente','nombre','apellidos','mail','direccion','ciudad_id','supermercado_id','id_user_id']
class ClientesList(generics.ListAPIView):
    queryset=Clientes.objects.all()
    serializer_class=ClientesSerializer

class PedidosSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pedidos
        fields=['id_pedido','fecha_Pedido','fecha_Entrega','estado','cliente_id']
class PedidosList(generics.ListAPIView):
    queryset=Pedidos.objects.all()
    serializer_class=PedidosSerializer

