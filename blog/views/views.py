from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from blog.models import *
import os
from rest_framework.views import APIView
from django.http import Http404
import datetime
import polars as pl
from django.http import FileResponse
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@csrf_exempt
def Login(request):
    return render(request, 'blog/login.html', {})#envio el html para imprimirlo

@csrf_exempt
def auth(request):#Funcion para comprobar si el usuario esta logeado
    if request.method == 'POST':#comprueba si se accede por medio de un metodo Post
        mail=request.POST["mail"]#recoge el valor del mail del formulario
        contr=request.POST["contr"]#recoge el valor de la contraseña del formulario
        username_Log=(User.objects.get(email=mail)).username
        user=authenticate(username=username_Log, password=contr)#usa la funcion authenticate() la cual devuelve el usuario donde se cumplen las condiciones
        if user is not None:#Condicional que evalua si el usuario ha sido encontrado
            login(request, user)#guarda el usuario en la sesion y lo establece como usuario activo
            return HttpResponseRedirect('/principal')#redirige a la pagina principal
        else:
            return HttpResponseRedirect('/login')#redirige al login de nuevo
    else:
        return("Acceso denegado")

def Principal(request):
    userLog=request.user#Selecciona el usuario que esta en la sesion
    usuarios=(User.objects.all())#guarda en una lista todos ls usuarios logeados
    return render(request, 'blog/principal.html', {'usuarioLog':userLog,'Lista_usuarios':usuarios})#Envia el request y pasa como parametros el usuario de la sesion y la list de usuarios
def Pantalla_hacerse_cliente(request):
    userLog=request.user
    return render(request, 'blog/clientes.html')

def datos_cliente(request):
    data={}#Crea diccionario para enviar al front
    if request.method == 'GET':#comprueba si se accede por medio de un metodo get
        usuarios=User.objects.all().values()#guarda en una lista todos ls usuarios logeados
        if len(usuarios)>0:#si hay mas de 0 usuarios ejecuta el siguiente 
            lista=list()#crea una lista vacia
            for i in usuarios:#recorre los usuarios
                datos=[i['id'],i["first_name"],i['last_name'],i['email'],i['is_staff'],i['is_active'],i['last_login'],i['date_joined']]#Crea una lista de listas con los datos de los usuarios
                lista.append(datos)#añade lso datos del usuario a la lista que enviaremos
            data["ok"]=lista#añade al diccionario la key "ok" y añade la lista final como value
        else:#si no hubiese usuarios guardaria el diccionario con la clave error
           data["error"]="no se han podido recoger datos de los clientes"
        
    else:#si accede por post no se ejecuta la funcion
        return("Acceso denegado")
    return JsonResponse(data)

def buscarSupermercado(request):
    data={}
    if request.method=='GET':
        supermercados=Supermercados.objects.all()#Consulta que devuelve todos los supermercados
        print (supermercados)
        lista=list()
        if(len(supermercados)>0):#Mira si hay supermercados
            for i in range(len(supermercados)):#bucle que recorre los supermercados
                cp=supermercados[i].ciudad.codigo_postal
                id=supermercados[i].id_supermercado
                nombre=supermercados[i].nombre
                datosSupers=[cp, nombre,id]#guarda los datos del supermercado en un diccionario
                lista.append(datosSupers)
            data["ok"]=lista#Guarda en un diccioaro dond la clave es un numero los datos de los supermercados
                
        else:
            data[0]="No hay supermercados"#Si no hay supermercados lo pone
    else:
        return("Acceso denegado")
    print(data,"\n\n")
    return JsonResponse(data)#Devuelve un Json con los datos

@csrf_exempt
def crearUser(request):
    data={}
    lista=list()
    if request.method=='POST':
        nombreCL=request.POST.get('name')
        apellidoCL=request.POST.get('apellido')
        mailCL=request.POST.get('email')
        contrCL=request.POST.get('contrasena')

        a = mailCL.find('@')
        b = mailCL.find('.')
        print(a, b)

        if((a == -1 or b == -1) or (a > b or a == b - 1) or (a == 0 or mailCL.endswith("."))):
           data={ 'error': 'Formato de mail incorrecto'}

        elif((nombreCL=='') or (apellidoCL =='') or (mailCL =='') or (contrCL =='')):#Comprueba si hay campos vacios
            data={ 'error': 'Campos vacios'}
        # print(len(User.objects.filter(email=mailCL).values()))
        
        elif User.objects.filter(email=mailCL): #Compruea si el mail ya existe en la BD 
            data={ 'error': 'El usuario ya existe'}
            
        else:
            
            user=User.objects.create_user(nombreCL,mailCL,contrCL)#Crea un usuario
            user.first_name=nombreCL#le da valor al nombre
            user.last_name=apellidoCL#le da valor al apellido
            user.save()#Guarda el usuario
            data={'ok':'Usuario añadido con exito'}
            idclUS=user.pk
            crearCliente(nombreCL,apellidoCL,mailCL,idclUS)
        return JsonResponse(data)

def crearCliente(name,ap,email,id):
    cliente= Clientes.objects.create(nombre=name,apellidos=ap,mail=email,id_user_id=id)

def modalAñadir(request):
    if request.method=='GET':
        fichero = open('blog/templates/blog/modal_anadir.html')#guarda el html en una variable
        cont=fichero.read()#guarda el contenid del html 
        cont=cont.replace('Ã±','ñ')
        data={ 'ok': 'true'}
        data['contenido']=cont
        return JsonResponse(data)#Devuelve un Json con los datos
    else:
        data={'error':'Metodo request incorrecto'}
        return JsonResponse(data)#Devuelve un Json con los datos

def modalBorrar(request):
    if request.method=='GET':
        fichero = open('blog/templates/blog/modal_borrar.html')#guarda el html en una variable
        cont=fichero.read()#guarda el contenid del html 
        data={ 'ok': 'true'}
        data['contenido']=cont
        cont=cont.replace('Ã±','ñ')
        return JsonResponse(data)#Devuelve un Json con los datos
    else:
        data={'error':''}
        return JsonResponse(data)#Devuelve un Json con los datos

def modalEditar(request):
    if request.method=='GET':
        fichero = open('blog/templates/blog/modal_editar.html')#guarda el html en una variable
        cont=fichero.read()#guarda el contenid del html
        cont=cont.replace('Ã±','ñ')
        data={ 'ok': 'true'}
        data['contenido']=cont
        return JsonResponse(data)#Devuelve un Json con los datos
    else:
        data={'error':''}
        return JsonResponse(data)#Devuelve un Json con los datos

@csrf_exempt
def borrarUser(request):
    if request.method=='POST':
        mail=request.POST.get('email')#toma el parametro pasado por post
        user=User.objects.get(email=mail)#Busca el usuario qeu tiene es mail
        user.delete();#lo elimina
        data={"ok":'borrado con exito'}
    else:
        data={'delete':"acceso denegado"}
    return JsonResponse(data)

def datosCompletos(request):
    data={}#Crea diccionario para enviar al front
    if request.method == 'GET':#comprueba si se accede por medio de un metodo get 
        usuarios=User.objects.all().values()#guarda en una lista todos ls usuarios logeados
        if len(usuarios)>0:#si hay mas de 0 usuarios ejecuta el siguiente 
            lista=list()#crea una lista vacia
            for i in usuarios:#recorre los usuarios
                datos=[i['username'],i["first_name"],i['last_name'],i['email'],i['password'],i['is_staff'],i['id']]#Crea una lista de listas con los datos de los usuarios
                lista.append(datos)#añade lso datos del usuario a la lista que enviaremos
            data["ok"]=lista#añade al diccionario la key "ok" y añade la lista final como value
        else:#si no hubiese usuarios guardaria el diccionario con la clave error
           data["error"]="no se han podido recoger datos de los clientes"
    else:
        data={'error':"metodo request no permitido"}
    return JsonResponse(data)

@csrf_exempt
def editarUser(request):
    data={}
    if request.method =='POST':#Evalua si el request es modo post
        print(request.POST)
        #Coge los parametrospasados por la peticion
        id=request.POST.get('id')
        username=request.POST.get('username')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password=request.POST.get('password')
        admin=request.POST.get('admin')

        a = email.find('@')
        b = email.find('.')
        print(a, b)

        if((a == -1 or b == -1) or (a > b or a == b - 1) or (a == 0 or email.endswith("."))):
           data={ 'error': 'Formato de mail incorrecto'}

        elif((first_name=='') or (last_name =='') or (email =='') or (password =='')or (username =='')):#Comprueba si hay campos vacios
            data={ 'error': 'Campos vacios'}
        else:
            user=User.objects.get(pk=id)#Busca el usuario que editar
            #Pone ,os valores nuevos al usuario
            user.username=username
            user.email=email
            user.first_name=first_name
            user.last_name=last_name

            if(user.password!=password):
                user.set_password(password)
            if(admin):
                user.is_staff=True
            else:
                user.is_staff=False
            #Guarda al usuario
            user.save()
            data={'ok':'Editado con exito'}
        
    else:
        data={'error': 'metodo request incorrecto'}
    
    return JsonResponse(data)

def crearExcel(request):
    data={}
    print("o")
    if request.method == 'GET':#Evalua si el request es modo posts
        usuarios=User.objects.all().values()#guarda en una lista todos ls usuarios logeados
        if len(usuarios)>0:#si hay mas de 0 usuarios ejecuta el siguiente 
            lista=list()#crea una lista vacia
            for i in usuarios:#recorre los usuarios
                datos=[i['id'],i["first_name"],i['last_name'],i['email']]#Crea una lista de listas con los datos de los usuarios

                lista.append(datos)#añade lso datos del usuario a la lista que enviaremos
            df = pl.DataFrame({#Crea la lista de una row con sus headers
                'id':str(lista[0][0]),
                'nombre':lista[0][1],
                'apellido':lista[0][2],
                'mail':lista[0][3],
                })
            i=1
            while i<len(lista):
                dfAux=pl.DataFrame({#Añade a la anterior lista los demas recursos
                    'id':str(lista[i][0]),
                    'nombre':lista[i][1],
                    'apellido':lista[i][2],
                    'mail':lista[i][3],
                })
                df=pl.concat([df,dfAux]) 
                i=i+1 
            x = datetime.datetime.now()#Fecha y hora del momento
            fecha=x.strftime('%x_%X')
            fecha=fecha.replace("/","-")
            fecha=fecha.replace(":","-")
            print(fecha)
            nombre_excel="listausuarios"+fecha+".xlsx"#Nombre del archivo
            path=crearPath(nombre_excel)
            url=crearUrl(nombre_excel)
            df.write_excel(#Crea la tabla y da formato y estilo  
                workbook=path,
                column_widths={"id": 125,"nombre": 125,"apellido": 125,"mail": 125},
                header_format={"bold":True, "font_color":"#702963","fg_color": "#D7E4BC","align":"center"},
            )
            data['url']=url#envia la url
            data['ok']='todo ok'
        else:
            data['error']='No hay usuarios'
    else:
        data['error']='metodo post incorrecto'
    
    return JsonResponse(data)  

def crearPath(nombrearchivo):#Crea la ruta donde se descargara el archivo
    media=settings.MEDIA_ROOT
    nombre_archivo=nombrearchivo
    path=os.path.join(media,nombre_archivo)
    return(path)
def crearUrl(nombrearchivo):#Crea la ruta donde descargar el archivo
    media="media"
    nombre_archivo=nombrearchivo
    url=os.path.join(media,nombre_archivo)
    return(url)

from rest_framework import viewsets
from serializers import *

class UserViewset(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = User.objects.all()
        username = self.request.query_params.get('username')
        id = self.request.query_params.get('id')
        email = self.request.query_params.get('email')
        print(self.request.query_params)
        if username is not None:
            queryset = queryset.filter(username=username)
        elif id is not None:
            queryset = queryset.filter(id=id)
        elif email is not None:
            queryset = queryset.filter(email=email)
        elif self.request.query_params!={}:
            queryset=[]
        return queryset
    def post_queryset(self):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CiudadesViewset(viewsets.ModelViewSet):
    queryset = Ciudades.objects.all()
    serializer_class = CiudadesSerializer

class SupersViewset(viewsets.ModelViewSet):
    queryset = Supermercados.objects.all()
    serializer_class = SuperSerializer

class ClientesViewset(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer
    

from rest_framework import status

class PedidosViewset(viewsets.ModelViewSet):
    queryset=Pedidos.objects.all()
    serializer_class=PedidosSerializer


class user_list(APIView):
    
    def get(self, request, format=None):
        
        usuarios=User.objects.all()
        serializer = UserSerializer(usuarios, many=True)
        return Response(serializer.data)
    @csrf_exempt
    def post(self, request, format=None):
        nombre=request.POST.get('first_name')
        apellido=request.POST.get('last_name')
        mail=request.POST.get('email')
        contr=request.POST.get('password')

        a = mail.find('@')
        b = mail.find('.')
        print(a, b)

        if((a == -1 or b == -1) or (a > b or a == b - 1) or (a == 0 or mail.endswith("."))):
           data={ 'error': 'Formato de mail incorrecto'}

        elif((nombre=='') or (apellido =='') or (mail =='') or (contr =='')):#Comprueba si hay campos vacios
            data={ 'error': 'Campos vacios'}
        # print(len(User.objects.filter(email=mailCL).values()))
        
        elif User.objects.filter(email=mail): #Compruea si el mail ya existe en la BD 
            data={ 'error': 'El usuario ya existe'}
            
        else:
            
            serializer = UserSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                data={ 'ok': ''}
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data)
    
    def delete(self, request, format=None):
        # mail=request.get('email')
        email=request.POST.get('email')
        usuarios=User.objects.get(email=email)
       
        usuarios.delete()
        return JsonResponse(data={'ok':"Eliminado con exito"})
        
        
class user_Detail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        usuario = self.get_object(pk)
        serializer = UserSerializer(usuario)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        usuario = self.get_object(pk)
        serializer = UserSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Editar_Usuario_API(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        id=request.POST.get('id')
        username=request.POST.get('username')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password=request.POST.get('password')
        admin=request.POST.get('admin')

        a = email.find('@')
        b = email.find('.')
        print(a, b)

        if((a == -1 or b == -1) or (a > b or a == b - 1) or (a == 0 or email.endswith("."))):
           data={ 'error': 'Formato de mail incorrecto'}

        elif((first_name=='') or (last_name =='') or (email =='') or (password =='')or (username =='')):#Comprueba si hay campos vacios
            data={ 'error': 'Campos vacios'}
        else:
            user=User.objects.get(pk=id)#Busca el usuario que editar
            #Pone ,os valores nuevos al usuario
            user.username=username
            user.email=email
            user.first_name=first_name
            user.last_name=last_name

            if(user.password!=password):
                user.set_password(password)
            if(admin):
                user.is_staff=True
            else:
                user.is_staff=False
            serializer = UserSerializer(user)
            if serializer.is_valid():
                data={'ok': ''}
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data)