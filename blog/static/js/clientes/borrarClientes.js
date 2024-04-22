
$(document).ready(function() {
    
    var botonB = document.getElementById("Borrar");
    botonB.addEventListener("click", function(){ //Evento onclick 
        console.log("click")
        $.ajax({//peticion ajax del html
            url:"Borrar/",
            type:"GET",
            data:{},//Lo que escriba dentro se pasara al .py como parametro 
            dataType:"json",
            success:function(data){
                if(data.ok!=undefined){  //evalua si los datos se han enviado correctamente               
                    $('body').append(data['contenido'])//añade al body el contenido del html
                    abrirmodalBorrar()//Ejecuta la funcion abrirmodal
                }
          }
        });
        
        
    });
});
function abrirmodalBorrar(url){//Funcion que abre el modal
    $('#modal_borrar').modal('show');//abre el modal con ese id
    clientes();
    $('#cerrarHB').click(function(){//Cuando se pulse el boton de cerrar se cerrara el modal y lo eliminara del html principal
        $('#modal_borrar').modal('hide');
        $('#modal_borrar').remove();//elimina el div del modal en el html
    })
    $('#cerrarB').click(function(){//Cuando se pulse el boton de cerrar del header se cerrara el modal y lo eliminara del html primcipal
        $('#modal_borrar').modal('hide');
        $('#modal_borrar').remove();//elimina el div del modal en el html
    })
    $('#borrarCL').click(function(){
        borrar();
        $('#modal_borrar').modal('hide');
        $('#modal_borrar').remove();//elimina el div del modal en el html
    })
}
function clientes(){
    $.ajax({
        url: "datos_cliente/",//url de la funcion
        type: "GET",//tipo de transaccion de datos
        data: {},
        dataType: 'json',//tipo de datos como pasamos un diccionario el tipo es json
        success: function (data) {//ejecuat una funcion que tiene como parametros los datos recogidos
            if(data.ok!=undefined){//Si los datos no estan vacios genera la tabla
                let usuarios = document.getElementById('clientes');//Busca en el formulario el cuadro de texto del codigo postal 
                ListaAux=data['ok'];//Crea una lista auxiliar donde almacena los usuarios de la clave ok
                var count = ListaAux.length;
                for(i=0;i<count;i++){
                    user=ListaAux[i]
                    console.log(user)
                    const opt1 = document.createElement("option");//Crea la opcion
                    opt1.value =user[3];
                    opt1.text = (user[3]);
                    usuarios.add(opt1,null);//Añade la opcion al select
                }
            }
            else{
                console.log("No hay clientes")
            }

        },error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr);
            console.log( ajaxOptions);
            console.log( thrownError);
        }
    });
}
function borrar(){
    let user = document.getElementById('clientes');
    var mail = user.options[user.selectedIndex].value;
    const datos ={
        email: mail,
    };
    $.ajax({
        url:"BorrarUsuarios/",
        type:"POST",
        data: datos,//Lo que escriba dentro se pasara al .py como parametro 
        dataType:"json",
        success:function(data){
            if(data.ok!=undefined){
                Swal.fire({
                    position: "top-end",
                    icon: "success",
                    title: "Borrado con exito",
                    showConfirmButton: false,
                    timer: 2500
                });
                console.log(data.ok)
                hot.destroy();
                datos_clientes();
            }
        }
        ,error: function () {
            console.log(data.error)
      }
      })
}