function buscarSuper(){
    $.ajax({
      url:"Supermercados/",
      type:"GET",
      data:{},//Lo que escriba dentro se pasara al .py como parametro 
      dataType:"json",
      success:function(data){
        let select_supers = document.getElementById('super_CL');//Busca en el formulario el cuadro de texto del codigo postal 
        var options = select_supers.options;//Guarda las opciones
        while (options.length>0) {//Bucle que esta activo mientras haya opciones
          select_supers.remove(0);//Elimina la primera opcion
        }
        let cp=document.getElementById('CP_CL').value;//almacena el valor del codigo postal
        ListaAux=data['ok'];//Crea una lista auxiliar donde almacena los supermercados de la clave ok
        var count = ListaAux.length;//Cuenta el numero de objetos en la lista
        for(i=0;i<count;i++){//Bucle para recorrer el Json      
          console.log(ListaAux[i])//imprime el supermercado
          sup=ListaAux[i]//Guarda los valores de la lista en esa posicion
          if(sup[0]==cp){//comprueba si el valor del bucle coincide con el codigo postal del elemento de la lista
            const opt1 = document.createElement("option");//Crea la opcion
               opt1.value =sup[2];
               opt1.text = sup[1];//Pone como texto de la opcion el nobmre del supermercado
               select_supers.add(opt1,null);//Añade la opcion al select
          }
        } 
      }
    })
  }
  $(document).ready(function() {
    var boton1 = document.getElementById("buscarSuper");
    boton1.addEventListener("click", function(){
        buscarSuper()
    });
  });