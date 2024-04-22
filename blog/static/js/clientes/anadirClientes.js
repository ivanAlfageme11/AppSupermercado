
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
    else if(a==0||mail.endsWith(".")){
        return false;
    }
    else{
        return true;
    }
    
}
$(document).ready(function() {
    
    var boton1 = document.getElementById("Añadir");
    boton1.addEventListener("click", function(){ //Evento onclick 
        console.log("click")
        $.ajax({//peticion ajax del html
            url:"Anadir/",
            type:"GET",
            data:{},//Lo que escriba dentro se pasara al .py como parametro 
            dataType:"json",
            success:function(data){
                if(data.ok!=undefined){  //evalua si los datos se han enviado correctamente               
                    
                    $('body').append(data['contenido'])//añade al body el contenido del html
                    abrirmodalAñadir()//Ejecuta la funcion abrirmodal
                }
          }
        });
        
        
    });
  });

  function abrirmodalAñadir(url){//Funcion que abre el modal
    $('#modal_anadir').modal('show');//abre el modal con ese id
    $('#cerrarAn').click(function(){//Cuando se pulse el boton de cerrar se cerrara el modal y lo eliminara del html principal
        $('#modal_anadir').modal('hide');
        $('#modal_anadir').remove();//elimina el div del modal en el html
    })
    $('#cerrarHAn').click(function(){//Cuando se pulse el boton de cerrar del header se cerrara el modal y lo eliminara del html primcipal
        $('#modal_anadir').modal('hide');
        $('#modal_anadir').remove();//elimina el div del modal en el html
    })
    $('#guardarAn').click(function(){//Cuando se pulse el boton de cerrar del header se cerrara el modal y lo eliminara del html primcipal

        const datos = { 
            name: $('#nombreCl').val(), 
            apellido: $('#apellidoCl').val(), 
            email: $('#mailCl').val(), 
            contrasena: $('#contrCL').val(), 
                
        };
        $.ajax({
            url:"AnadirUsuarios/",
            type:"POST",
            data: datos,//Lo que escriba dentro se pasara al .py como parametro 
            dataType:"json",
            success:function(data){
                if(data.error!=undefined){
                    if(!validarmail($('#mailCl').val())){
                        Swal.fire({
                            icon: "error",
                            title: "Error",
                            text: "Formato de mail incorrecto",                                
                        });
                    }
                    else if(data.error=="El usuario ya existe"){
                        Swal.fire({
                            icon: "error",
                            title: "Error",
                            text: "El usuario ya existe",                                
                        });
                    }
                    else if(data.error=="Campos vacios"){
                        Swal.fire({
                            icon: "error",
                            title: "Error",
                            text: "Hay campos vacios",    
                        });
                    }
                }
                else{
                    console.log(data)
                    hot.destroy();
                    datos_clientes();
                    Swal.fire({
                        position: "top-end",
                        icon: "success",
                        title: "Añadido con exito",
                        showConfirmButton: false,
                        timer: 2500
                    });
                    $('#modal_anadir').modal('hide');
                    $('#modal_anadir').remove();//elimina el div del modal en el html
                }

            }
            ,error: function () {
                if(data.error!=undefined){
                    console.log(data.error)
                }
                else{
                    Swal.fire({
                        icon: "warning",
                        icon: "success",
                        title: "Algo salio mal",
                        showConfirmButton: false,
                        timer: 2500
                    });
                }
            }
        })  
    })
  }
