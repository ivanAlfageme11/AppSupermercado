var columnasColapsadas = [];
var columnasExpandidas = [];
colColaps=[]
var hot=null;
datos=[]
colapsed=true
expanded=false
function generartabla(dat){
  var container = document.getElementById('example');
  datos=dat
  datos_sin_id=datos;
  for(n=0;n<datos_sin_id.length;n++){
        datos_sin_id[n][0]=""
  }
  hot = new Handsontable(container, {
      data: datos,
      width: 800,
      height: 'auto',
      colHeaders: true,
      manualColumnResize: true,
      rowHeaders: false,
      colWidths: 200,
      rowHeights: 50,
      disableVisualSelection:true,
      dropdownMenu: true,
      // colHeaders:['id','Nombre', 'Apellido', 'mail',''],
      nestedHeaders: [
        ['id', {label: 'Nombre Completo', colspan: 2},{label: 'Email', colspan: 1},{label: 'Datos adicionales', colspan: 4},'Opciones',],
        
        ['id','Nombre', 'Apellido', '', 'Admin','Active', 'Last_Login','Create date', '']
      ],
      collapsibleColumns: true,

      collapsibleColumns: [
        { row: -2, col: 1, collapsible: true },//NombreCompleto
        { row: -2, col: 4, collapsible: true },
      ],
      autoWrapRow: true,
      autoWrapCol: false,
      className: 'htCenter htMiddle',
      filters: true,
      dateFormat: 'MM/DD/YYYY',
      correctFormat: true,
      hiddenColumns: {
        // specify columns hidden by default
        columns: [0]
      },   
      columns: [
        {},{renderer: cuerpo},{renderer: cuerpo},{renderer: cuerpo},{renderer: cuerpo},{renderer: cuerpo},{renderer: cuerpo},{renderer: cuerpo},{renderer: safeHtmlRenderer}
      ],
      afterDropdownMenuShow(instance) {
        var filters = instance.hot.getPlugin('filters');
        console.log(filters.valueComponent)
        filters.components.get('filter_by_value').elements[0].onClearAllClick({preventDefault: function() {}});
      },
      licenseKey: 'non-commercial-and-evaluation',
      afterChange: (changes) => {
        changes?.forEach(([row, prop, oldValue, newValue]) => {
          console.log(datos[prop][row])
          console.log(oldValue)
          if(datos[prop][row]==oldValue){
            datos[prop][row]=newValue
            console.log(datos[prop][row])
          }
          else{
            console.log('no coinciden')
          }
        });
      }, // for non-commercial use only
  });
  var filters = hot.getPlugin('filters');
  
  header();

  window.hot = hot;
  window.filters = filters;
  function customRenderer(hotInstance, td, row, column, prop, value, cellProperties) {
    // Optionally include `BaseRenderer` which is responsible for
    // adding/removing CSS classes to/from the table cells.
    Handsontable.renderers.BaseRenderer.apply(this, arguments);
  } 
  function safeHtmlRenderer(instance, td, row, col, prop, value, cellProperties) {
    // WARNING: Be sure you only allow certain HTML tags to avoid XSS threats.
    // Sanitize the "value" before passing it to the innerHTML property.
    td.style.background = '#dcff7bc2';
    td.innerHTML = '<div class="row m-2"> <div class="col mx-auto"><button data-id="'+datos[row][0]+'"data-row="'+row+'"class="editarEVNT btn btn-warning btn-sm rounded-circle"><i class="fas fa-pen fa-lg"></i></button></div>'+
                  '<div class="col"><button data-id="'+datos[row][0]+'"data-row="'+row+'"class="borrarEVNT btn btn-danger btn-sm rounded-circle"><i class="far fa-trash-alt"></i></button></div></div>';
  }
  function cuerpo(instance, td, row, col, prop, value, cellProperties) {
    // WARNING: Be sure you only allow certain HTML tags to avoid XSS threats.
    // Sanitize the "value" before passing it to the innerHTML property.
    Handsontable.renderers.TextRenderer.apply(this, arguments);
    td.style.background = '#dcff7bc2';
    td.style.color='black'
  }
  //Actualiza lista con las columnas que estan colapsadas
  Handsontable.hooks.add('afterColumnCollapse',function(currentCollapsedColumns, destinationCollapsedColumns, collapsePossible, successfullyCollapsed){
    columnasColapsadas = destinationCollapsedColumns;
    console.log("Columnas colapsadas: ",destinationCollapsedColumns)    
});
//Despues de que una columna se expanda guarda las columnas colapsadas en una lista
Handsontable.hooks.add('afterColumnExpand',function(currentCollapsedColumns, destinationCollapsedColumns, expandPossible, successfullyExpanded){
    
    columnasColapsadas = destinationCollapsedColumns;
    console.log("Columnas colapsadas: ",columnasColapsadas)        
});	

  console.log('aaa') 
  
  
  cargarBotones();
}
function datos_clientes(){
  $.ajax({
    url: "datos_cliente/",//url de la funcion
    type: "GET",//tipo de transaccion de datos
    data: {},
    dataType: 'json',//tipo de datos como pasamos un diccionario el tipo es json
    success: function (data) {//ejecuat una funcion que tiene como parametros los datos recogidos
        if(data.ok!=undefined){//Si los datos no estan vacios genera la tabla
          datos=(data.ok)
          generartabla(datos)//genera la tabla con la lista que pertenece al valor de la key "ok"
          
        }
        else{
          console.log("No hay datos")
        }

    },error: function (xhr, ajaxOptions, thrownError) {
        console.log(xhr);
        console.log( ajaxOptions);
        console.log( thrownError);
    }
  });
}

$(document).ready(function() {
    
    datos_clientes()
    $('#Actualizar').on('click',function(){
      actualizar();
    })
    $('#Export').on('click',function(){
      url="";
      $.ajax({
        url: "Exportar/",//url de la funcion
        type: "GET",//tipo de transaccion de datos
        data: {},
        dataType: 'json',//tipo de datos como pasamos un diccionario el tipo es json
        success: function (data) {//ejecuat una funcion que tiene como parametros los datos recogidos
          if(data.ok!=undefined){
            console.log("0")
              if(data['url']!=undefined){
                url=data['url'];
                url=url.replace('\\','/')
                console.log(url)
                window.open( "/"+url,'download')
              }
          }
          else if(data.error!=undefined){
            Swal.fire({
              position: "top-end",
              icon: "info",
              text: data.error,
              showConfirmButton: false,
              timer: 2500
          });
          }   
          
        },error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr);
            console.log( ajaxOptions);
            console.log( thrownError);
        }
      });
    })
    function cargarTabla(data) {
      if (hot) {
          hot.loadData(data); // Si la tabla ya está cargada, simplemente cargamos los nuevos datos
          cargarBotones();
        } else {
        datos_clientes();
      }
    }
    function filtrarTabla(valor) {
      datos=datos_sin_id
      var datosFiltrados = datos.filter(function(fila) {
        return fila.some(function(celda) {
          return celda.toString().toLowerCase().includes(valor.toLowerCase().trim());
        });
      });
      cargarTabla(datosFiltrados);
    }
    var inputBusqueda = document.querySelector('.FT');
    var boton=document.getElementById("buscar")
    boton.addEventListener("click", function(){
        filtrarTabla(inputBusqueda.value);
    })
    var boton=document.getElementById("limpiarFiltro")
    boton.addEventListener("click", function(){
      inputBusqueda.value=""
      filtrarTabla(inputBusqueda.value);
    })
    // var inputBusqueda = document.querySelector('.FT');//variable del input text
    // inputBusqueda.addEventListener('input', function() {//Crea la funcion que se ejecuta cuando el texto cambia
    //   filtrarTabla(this.value);//ejecuta filtrar tabla con el valor del input text
    // });
});
function cargarBotones(){
  setTimeout(function(){
    $('.editarEVNT').on('click',function(){
        var row=$(this).data("row");
        console.log(row)
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
      })
  },200);
setTimeout(function(){
  $('.borrarEVNT').on('click',function(){
    var row=$(this).data("row");
    $.ajax({//peticion ajax del html
      url:"Borrar/",
      type:"GET",
      data:{},//Lo que escriba dentro se pasara al .py como parametro 
      dataType:"json",
      success:function(data){
          if(data.ok!=undefined){  //evalua si los datos se han enviado correctamente               
              $('body').append(data['contenido'])//añade al body el contenido del html
              abrirmodalBorrar(row)//Ejecuta la funcion abrirmodal
          }
      }
    });
  })
},200)
}
function header(){
  colColaps=columnasColapsadas
  
  hot.getPlugin('collapsibleColumns').collapseAll();
  if(colColaps.length!=0){
    console.log(colColaps)
    hot.getPlugin('collapsibleColumns').expandAll();
    for(i=0;i<colColaps.length;i++){
      n=colColaps[i]
      console.log("columna del for",n)
      hot.getPlugin('collapsibleColumns').collapseSection({row: -2, col: (n-1)});
    }
  }
}
function actualizar(){
  hot.destroy(); 
       
      datos_clientes();
      cerrarHeader();
}

  