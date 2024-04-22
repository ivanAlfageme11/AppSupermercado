

function validarmail(mail){
    
    a=mail.indexOf('@');
    b=mail.indexOf('.');
    console.log(a)
    console.log(b)
    console.log()
    if(a==-1 || b==-1){
        return false;
    }
    else if(a>b || a==b-1){
        return false;
    }
    else if(a==0 || mail.endsWith(".")){
        return false;
    }
    else{
        return true;
    }
    
}

$(document).ready(function() {
    
    var button = document.querySelector('.editarEVNT');
    button.addEventListener('click', function(){
        var row=0
        console.log('l')
        $.ajax({//peticion ajax del html
            url:"Editar/",
            type:"GET",
            data:{},//Lo que escriba dentro se pasara al .py como parametro 
            dataType:"json",
            success:function(data){
                if(data.ok!=undefined){  //evalua si los datos se han enviado correctamente               
                    $('body').append(data['contenido'])//añade al body el contenido del html
                    abrirmodalEditar(row)//Ejecuta la funcion abrirmodal
                }
            }
        });
    });
});
var id;
function abrirmodalEditar(row){//Funcion que abre el modal
    $('#modal_editar').modal('show');//abre el modal con ese id
        Campos(row);
        
    $('#cerrarHED').click(function(){//Cuando se pulse el boton de cerrar se cerrara el modal y lo eliminara del html principal
        $('#modal_editar').modal('hide');
        $('#modal_editar').remove();//elimina el div del modal en el html
    })
    $('#cerrarED').click(function(){//Cuando se pulse el boton de cerrar del header se cerrara el modal y lo eliminara del html primcipal
        $('#modal_editar').modal('hide');
        $('#modal_editar').remove();//elimina el div del modal en el html
    })
    $('#clear').click(function(){//Cuando se pulse el boton de cerrar del header se cerrara el modal y lo eliminara del html primcipal
        var username=document.getElementById('Ed_username')
        var mail=document.getElementById('Ed_mail')
        var nombre=document.getElementById('Ed_nombre')
        var apellido=document.getElementById('Ed_apellido')
        var contr=document.getElementById('Ed_contraseña')
        var adminT=document.getElementById('Admintrue')
        var adminF=document.getElementById('Adminfalse')
        
        username.value=''
        nombre.value=''
        apellido.value=''
        mail.value=''
        contr.value=''
        adminT.checked = false;
        adminF.checked = false;
    })
    $('#guardarED').click(function(){    
            
        Editar();//Ejecuta editar      
    
    });
}
function Campos(row){
    var username=document.getElementById('Ed_username')
    var mail=document.getElementById('Ed_mail')
    var nombre=document.getElementById('Ed_nombre')
    var apellido=document.getElementById('Ed_apellido')
    var contr=document.getElementById('Ed_contraseña')
    var adminT=document.getElementById('Admintrue')
    var adminF=document.getElementById('Adminfalse')
    $.ajax({
        url: "DatosCompletos/",//url de la funcion
        type: "GET",//tipo de transaccion de datos
        data: {},
        dataType: 'json',//tipo de datos como pasamos un diccionario el tipo es json
        success: function (data) {//ejecuat una funcion que tiene como parametros los datos recogidos
            if(data.ok!=undefined){//Si los datos no estan vacios genera la tabla
                user=[data['ok']][0][row]//El primer corchete siempre sera 0 porque es donde  esta la lista con los datos, el segundo corchete marca la posicion de la lista, cada uno es un usauario diferente
                id=user[6]
                //Guarda los datos
                username.value=user[0]
                nombre.value=user[1]
                apellido.value=user[2]
                mail.value=user[3]
                contr.value=user[4]
                
                if(value=user[5]){
                    adminT.checked = true;//Comprueba si es admin y lo pone a true si es correcto
                }
                else{
                    adminF.checked = true;//Comprueba si no es admin y lo pone a true si es correcto
                }
                
            }
            else{
              
            }
    
        },error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr);
            console.log( ajaxOptions);
            console.log( thrownError);
        }
      });
      
}

function Editar(){

    var adminT=document.getElementById('Admintrue')
    
    var admin;
    if(adminT.checked)//Comprueba si es admin
        admin=true
    else
        admin=false


    datos={
        'id':id,
        'username':document.getElementById('Ed_username').value,
        'mail':document.getElementById('Ed_mail').value,
        'first_name':document.getElementById('Ed_nombre').value,
        'last_name':document.getElementById('Ed_apellido').value,
        'contr':document.getElementById('Ed_contraseña').value,
        'admin':admin,
    };
    $.ajax({
        url:"EditarUsuarios/",
        type:"POST",
        data: datos,//Lo que escriba dentro se pasara al .py como parametro 
        dataType:"json",
        success:function(data){
            
            if(data.error!=undefined)
                if(data.error= 'Campos vacios'){
                    Swal.fire({
                        icon: "error",
                        title: "Error",
                        text: "Hay campos vacios",
                        
                    });
                } 
                else if(data.error='El usuario ya existe'){
                    Swal.fire({
                        icon: "error",
                        title: "Error",
                        text: "El usuario ya existe",                                
                    });
                }
            if(data.ok!=undefined){
                Swal.fire({
                    position: "top-end",
                    icon: "success",
                    title: "Editado con exito",
                    showConfirmButton: false,
                    timer: 2500
                });
                console.log(data.ok)
                $('#modal_editar').modal('hide');//Cierra el modal
                $('#modal_editar').remove();
                hot.destroy();
                datos_clientes();
            }
        },
        error: function () {
            
            console.log(data.error)
        }
    });
}