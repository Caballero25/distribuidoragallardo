function table_export(table, pages, filename, formats, time_reload) {
    // Log table element for debugging
    console.log($(table));

    // Initialize an empty array for button formats
    const botones = [];

    // Define button configurations based on formats array
    formats.forEach(format => {
        switch (format) {
            case 'excel':
                botones.push({
                    extend: 'excel',
                    text: '<i class="fa fa-file-excel-o"></i> Exportar a Excel',
                    titleAttr: 'Excel',
                    className: 'btn btn-success',
                    title: filename,
                    exportOptions: {
                        columns: ':visible',
                        format: {
                            body: function (data) {
                                // Convert data to text and handle numeric formatting
                                data = $('<p>' + data + '</p>').text();
                                return $.isNumeric(data.replace(',', '.')) ? data.replace(',', '.') : data;
                            }
                        }
                    }
                });
                break;
            case 'csv':
                botones.push({
                    extend: 'csv',
                    text: '<i class="fa fa-file-text-o"></i> Exportar a CSV',
                    titleAttr: 'CSV',
                    className: 'btn btn-info',
                    title: filename
                });
                break;
            case 'print':
                botones.push({
                    extend: 'print',
                    text: '<i class="fa fa-print"></i> Imprimir',
                    titleAttr: 'Imprimir',
                    className: 'btn btn-primary',
                    title: filename
                });
                break;
            case 'pdf':
                botones.push({
                    extend: 'pdf',
                    text: '<i class="fa fa-file-pdf-o"></i> Exportar a PDF',
                    titleAttr: 'PDF',
                    className: 'btn btn-danger',
                    title: filename
                });
                break;
        }
    });

    // Set up auto-reload if time_reload is greater than 0
    if (time_reload > 0) {
        setInterval(() => location.reload(), time_reload);
    }

    // Initialize DataTable with configuration
    const tabla = $(table).DataTable({
        language: {
            sProcessing: "Procesando...",
            sLengthMenu: "Mostrar _MENU_ registros",
            sZeroRecords: "No se encontraron resultados",
            sEmptyTable: "Ningún dato disponible en esta tabla",
            sInfo: "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            sInfoEmpty: "Mostrando registros del 0 al 0 de un total de 0 registros",
            sInfoFiltered: "(filtrado de un total de _MAX_ registros)",
            sSearch: "Buscar:",
            sLoadingRecords: "Cargando...",
            oPaginate: {
                sFirst: "Primero",
                sLast: "Último",
                sNext: "Siguiente",
                sPrevious: "Anterior"
            },
            oAria: {
                sSortAscending: ": Activar para ordenar la columna de manera ascendente",
                sSortDescending: ": Activar para ordenar la columna de manera descendente"
            }
        },
        lengthMenu: [[pages, 25, 50, -1], [pages, 25, 50, "Todos"]],
        dom: 'Bfrtip',
        buttons: botones
    });

    // Row selection handler
    $(table + ' tbody').on('click', 'tr', function () {
        $(this).toggleClass('selected').siblings().removeClass('selected');
    });
}



function table_no_pages(table, filename, formats, time_reload) {
    formatos = []
    for (i = 0; i < formats.length; i++) {
        if (formats[i] === 'excel') {
            formatos.push({
                extend: 'excel',
                text: '<i class="fa fa-file-excel-o"></i> Exportar a Excel',
                titleAttr: 'Excel',
                className: 'btn btn-success',
                title: filename,
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function (data, row, column, node) {
                            data = $('<p>' + data + '</p>').text();
                            return $.isNumeric(data.replace(',', '.')) ? data.replace(',', '.') : data;
                        }
                    }
                }
            })
        }
        if (formats[i] === 'csv') {
            formatos.push({
                extend: 'csv',
                text: '<i class="fa fa-file-text-o"></i> Exportar a CSV',
                titleAttr: 'CSV',
                className: 'btn btn-info',
                title: filename
            })
        }
        if (formats[i] === 'print') {
            formatos.push({
                extend: 'print',
                text: '<i class="fa fa-print"></i> Imprimir',
                titleAttr: 'Imprimir',
                className: 'btn btn-primary',
                title: filename
            })
        }
        if (formats[i] === 'pdf') {
            formatos.push({
                extend: 'pdf',
                text: '<i class="fa fa-file-pdf-o"></i> Exportar a PDF',
                titleAttr: 'PDF',
                className: 'btn btn-danger',
                title: filename
            })
        }
    }
   
    var tabla = $(table).DataTable({
        "language": {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "sZeroRecords": "No se encontraron resultados",
            "sEmptyTable": "Ningún dato disponible en esta tabla",
            "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Último",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        },
        "paging":   false,
        dom: 'Bfrtip',
        buttons: formatos
    });
    $(table + ' tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            tabla.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });
}

function table_no_row_select(table, pages, filename, formats, time_reload) {
    formatos = []
    for (i = 0; i < formats.length; i++) {
        if (formats[i] === 'excel') {
            formatos.push({
                extend: 'excel',
                text: '<i class="fa fa-file-excel-o"></i> Exportar a Excel',
                titleAttr: 'Excel',
                className: 'btn btn-success',
                title: filename,
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function (data, row, column, node) {
                            data = $('<p>' + data + '</p>').text();
                            return $.isNumeric(data.replace(',', '.')) ? data.replace(',', '.') : data;
                        }
                    }
                }
            })
        }
        if (formats[i] === 'csv') {
            formatos.push({
                extend: 'csv',
                text: '<i class="fa fa-file-text-o"></i> Exportar a CSV',
                titleAttr: 'CSV',
                className: 'btn btn-info',
                title: filename
            })
        }
        if (formats[i] === 'print') {
            formatos.push({
                extend: 'print',
                text: '<i class="fa fa-print"></i> Imprimir',
                titleAttr: 'Imprimir',
                className: 'btn btn-primary',
                title: filename
            })
        }
        if (formats[i] === 'pdf') {
            formatos.push({
                extend: 'pdf',
                text: '<i class="fa fa-file-pdf-o"></i> Exportar a PDF',
                titleAttr: 'PDF',
                className: 'btn btn-danger',
                title: filename
            })
        }
    }

    var tabla = $(table).DataTable({
        "language": {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "sZeroRecords": "No se encontraron resultados",
            "sEmptyTable": "Ningún dato disponible en esta tabla",
            "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Último",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        },
        "lengthMenu": [[pages, 25, 50, -1], [pages, 25, 50, "All"]],
        dom: 'Bfrtip',
        buttons: formatos
    });
}
 
function table_export_filters(table, pages, filename, formats, time_reload) {
    formatos = []
    for (i = 0; i < formats.length; i++) {
        if (formats[i] === 'excel') {
            formatos.push({
                extend: 'excel',
                text: '<i class="fa fa-file-excel-o"></i><svg xmlns="http://www.w3.org/2000/svg" class="icon icon-md" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"></path><polyline points="14 3 14 8 19 8"></polyline><path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z"></path><path d="M10 12l4 4m0 -4l-4 4"></path></svg> Exportar a Excel',
                titleAttr: 'Excel',
                className: 'btn btn-success',
                title: filename,
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function (data, row, column, node) {
                            data = $('<p>' + data + '</p>').text();
                            return $.isNumeric(data.replace(',', '.')) ? data.replace(',', '.') : data;
                        }
                    }
                }
            })
        }
        if (formats[i] === 'csv') {
            formatos.push({
                extend: 'csv',
                text: '<i class="fa fa-file-text-o"></i> Exportar a CSV',
                titleAttr: 'CSV',
                className: 'btn btn-info',
                title: filename
            })
        }
        if (formats[i] === 'print') {
            formatos.push({
                extend: 'print',
                text: '<i class="fa fa-print"></i><svg xmlns="http://www.w3.org/2000/svg" class="icon icon-md" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"></path><path d="M17 17h2a2 2 0 0 0 2 -2v-4a2 2 0 0 0 -2 -2h-14a2 2 0 0 0 -2 2v4a2 2 0 0 0 2 2h2"></path><path d="M17 9v-4a2 2 0 0 0 -2 -2h-6a2 2 0 0 0 -2 2v4"></path><rect x="7" y="13" width="10" height="8" rx="2"></rect></svg> Imprimir',
                titleAttr: 'Imprimir',
                className: 'btn btn-primary',
                title: filename
            })
        }
        if (formats[i] === 'pdf') {
            formatos.push({
                extend: 'pdf',
                text: '<i class="fa fa-file-pdf-o"></i> Exportar a PDF',
                titleAttr: 'PDF',
                className: 'btn btn-danger',
                title: filename
            })
        }
     
    }
    if (time_reload !== 0) {
        setInterval(function () {
            location.reload();
        }, time_reload);
    }

    var tabla = $(table).DataTable({
        "language": {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "sZeroRecords": "No se encontraron resultados",
            "sEmptyTable": "Ningún dato disponible en esta tabla",
            "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Último",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        },
        "lengthMenu": [[pages, 25, 50, -1], [pages, 25, 50, "All"]],
        dom: 'Bfrtip',
        buttons: formatos, 
    });
    $(table + ' tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            tabla.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });
}

function table_export_data(table, pages, filename, formats, time_reload, data) {
    formatos = []
    for (i = 0; i < formats.length; i++) {
        if (formats[i] === 'excel') {
            formatos.push({
                extend: 'excel',
                text: '<i class="fa fa-file-excel-o"></i> Exportar a Excel',
                titleAttr: 'Excel',
                className: 'btn btn-success',
                title: filename,
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function (data, row, column, node) {
                            data = $('<p>' + data + '</p>').text();
                            return $.isNumeric(data.replace(',', '.')) ? data.replace(',', '.') : data;
                        }
                    }
                }
            })
        }
        if (formats[i] === 'csv') {
            formatos.push({
                extend: 'csv',
                text: '<i class="fa fa-file-text-o"></i> Exportar a CSV',
                titleAttr: 'CSV',
                className: 'btn btn-info',
                title: filename
            })
        }
        if (formats[i] === 'print') {
            formatos.push({
                extend: 'print',
                text: '<i class="fa fa-print"></i> Imprimir',
                titleAttr: 'Imprimir',
                className: 'btn btn-primary',
                title: filename
            })
        }
        if (formats[i] === 'pdf') {
            formatos.push({
                extend: 'pdf',
                text: '<i class="fa fa-file-pdf-o"></i> Exportar a PDF',
                titleAttr: 'PDF',
                className: 'btn btn-danger',
                title: filename
            })
        }
    }
    if (time_reload !== 0) {
        setInterval(function () {
            location.reload();
        }, time_reload);
    }

    var tabla = $(table).DataTable({
         data:data,
        "language": {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "sZeroRecords": "No se encontraron resultados",
            "sEmptyTable": "Ningún dato disponible en esta tabla",
            "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Último",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        },
        "lengthMenu": [[pages, 25, 50, -1], [pages, 25, 50, "All"]],
        dom: 'Bfrtip',
        buttons: formatos,
        "bDestroy":true
    });
    $(table + ' tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            tabla.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });
}
