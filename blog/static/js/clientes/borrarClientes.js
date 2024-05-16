function abrirmodalBorrar(row){//Funcion que abre el modal
    $('#modal_borrar').modal('show');//abre el modal con ese id
    clientes(row);
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
function clientes(row){
    $.ajax({
        url: "http://127.0.0.1:9000/tabla/",//url de la funcion
        type: "GET",//tipo de transaccion de datos
        data: {},
        dataType: 'json',//tipo de datos como pasamos un diccionario el tipo es json
        success: function (data) {//ejecuat una funcion que tiene como parametros los datos recogidos
            console.log(data)
            //Si los datos no estan vacios genera la tabla 
                ListaAux=data['ok'];//Crea una lista auxiliar donde almacena los usuarios de la clave ok
                console.log(data['ok'])
                user=ListaAux[row]
                console.log(user)
                Tuser=document.getElementById('usuario')
                Tuser.value=user[3]
        

        },error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr);
            console.log( ajaxOptions);
            console.log( thrownError);
        }
    });
}
function borrar(id){
    var mail = document.getElementById('usuario').value;
    const datos={
        email:mail
    };
    $.ajax({
        url:"http://127.0.0.1:9000/users/",      
        type:"DELETE",
        data: datos,//Lo que escriba dentro se pasara al .py como parametro 
        dataType:"json",
        success:function(data){
            if(data.ok!=undefined){
                Swal.fire({
                    position:"top-end",
                    icon: "success",
                    title: data.ok,
                    showConfirmButton: false,
                    timer: 2500
                });
                console.log(data.ok)
                hot.destroy();
                datos_clientes();
            }
        }
        ,error: function () {

      }
      })
}