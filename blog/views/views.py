from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from blog.models import *
import os
import datetime
import polars as pl
from django.http import FileResponse
import requests
from django.conf import settings
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
                datos=[i['id'],i["first_name"],i['last_name'],i['email']]#Crea una lista de listas con los datos de los usuarios
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

# def Comprobar_cliente(request):
@csrf_exempt
def crearUser(request):
    data={}
    lista=list()
    if request.method=='POST':
        nombreCL=request.POST.get('name')
        apellidoCL=request.POST.get('apellido')
        mailCL=request.POST.get('email')
        contrCL=request.POST.get('contrasena')

        if((nombreCL=='') or (apellidoCL =='') or (mailCL =='') or (contrCL =='')):#Comprueba si hay campos vacios
            data={ 'error': 'Campos vacios'}
        # print(len(User.objects.filter(email=mailCL).values()))
        
        elif User.objects.filter(email=mailCL): #Compruea si el mail ya existe en la BD 
            print('errp')
            data={ 'error': 'El usuario ya existe'}
            
        else:
            user=User.objects.create_user(nombreCL,mailCL,contrCL)#Crea un usuario
            user.first_name=nombreCL#le da valor al nombre
            user.last_name=apellidoCL#le da valor al apellido
            user.save()#Guarda el usuario
            data={'ok':''}
        return JsonResponse(data)

def modalAñadir(request):
    if request.method=='GET':
        fichero = open('blog/templates/blog/modal_anadir.html')#guarda el html en una variable
        cont=fichero.read()#guarda el contenid del html 
        cont=cont.replace('Ã±','ñ')
        data={ 'ok': 'true'}
        data['contenido']=cont
        return JsonResponse(data)#Devuelve un Json con los datos
    else:
        data={'error':''}
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
    if request.method =='POST':
        print(request.POST)
        id=request.POST.get('id')
        username=request.POST.get('username')
        mail=request.POST.get('mail')
        nombre=request.POST.get('first_name')
        apellido=request.POST.get('last_name')
        contr=request.POST.get('contr')
        admin=request.POST.get('admin')
        if((username=='') or (mail =='') or (nombre =='') or (apellido =='')or (contr =='')or (admin =='')):
            data={ 'error': 'Campos vacios'}
        
        else:
            user=User.objects.get(pk=id)    
            user.username=username
            user.email=mail
            user.first_name=nombre
            user.last_name=apellido

            if(user.password!=contr):
                user.set_password(contr)
            if(admin):
                user.is_staff=True
            else:
                user.is_staff=False
            user.save()
            data={'ok':' '}
        
    else:
        data={'error': 'metodo request incorrecto'}
    
    return JsonResponse(data)

