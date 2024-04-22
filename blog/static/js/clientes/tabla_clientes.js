var hot=null;

function generartabla(datos){
  
  var container = document.getElementById('example');
  hot = new Handsontable(container, {
    data: datos,
    width: 'auto',
    height: 'auto',
    colHeaders: true,
    manualColumnResize: true,
    rowHeaders: false,
    colWidths: 200,
    rowHeights: 50,
    disableVisualSelection:true,
    dropdownMenu: true,
    colHeaders:['id','Nombre', 'Apellido', 'mail'],
    className: 'htCenter htMiddle',
    hiddenColumns: {
      // specify columns hidden by default
      columns: [0]
    },
    columns: [
      {},{},{},{},{renderer: safeHtmlRenderer}
  ],
    licenseKey: 'non-commercial-and-evaluation' // for non-commercial use only
    
  });
  function customRenderer(hotInstance, td, row, column, prop, value, cellProperties) {
    // Optionally include `BaseRenderer` which is responsible for
    // adding/removing CSS classes to/from the table cells.
    Handsontable.renderers.BaseRenderer.apply(this, arguments);
  }
  function safeHtmlRenderer(instance, td, row, col, prop, value, cellProperties) {
    // WARNING: Be sure you only allow certain HTML tags to avoid XSS threats.
    // Sanitize the "value" before passing it to the innerHTML property.
    
    td.innerHTML = '<button style="width:100%;height:100%;"data-id="'+datos[row][0]+'"data-row="'+row+'" class="editarEVNT">Editar</button>';
  }
  
}
function datos_clientes(){

  $.ajax({
    url: "datos_cliente/",//url de la funcion
    type: "GET",//tipo de transaccion de datos
    data: {},
    dataType: 'json',//tipo de datos como pasamos un diccionario el tipo es json
    success: function (data) {//ejecuat una funcion que tiene como parametros los datos recogidos
        if(data.ok!=undefined){//Si los datos no estan vacios genera la tabla
          generartabla(data.ok)//genera la tabla con la lista que pertenece al valor de la key "ok"
          // actualizarTabla()
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
});