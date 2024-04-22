// $(document).ready(function() {
//     var boton1 = document.getElementById("guardar");
//     boton1.addEventListener("click", function(){
//         console.log("funciona")
//         $(function(){
//             nuevoUsuario();
//             $('#modal_añadir').modal('hide');
//             $('#modal_anadir').remove();//elimina el div del modal en el html
//         });
//     });
//   });

//   function nuevoUsuario(){
//     const datos = { 
//         name: $('#nombreCl').val(), 
//         apellido: $('#apellidoCl').val(), 
//         email: $('#mailCl').val(), 
//         contrasena: $('#contrCL').val(), 
        
//     };
//     $.ajax({
//         url:"AnadirUsuarios/",
//         type:"POST",
//         data: datos,//Lo que escriba dentro se pasara al .py como parametro 
//         dataType:"json",
//         success:function(data){
//           console.log(data)
//         }
//       })
//   }