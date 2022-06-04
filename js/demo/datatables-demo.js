// Call the dataTables jQuery plugin
function filterGlobal() {
    $('#dataTable').DataTable().search(
        $('#global_filter').val(),
        $('#global_regex').prop('checked'),
        $('#global_smart').prop('checked')
    ).draw();
}

function filterColumn(i) {
    $('#dataTable').DataTable().column(i).search(
        $('#col' + i + '_filter').val(),
        $('#col' + i + '_regex').prop('checked'),
        $('#col' + i + '_smart').prop('checked')
    ).draw();
}

$(document).ready(function () {
    var table = $('#dataTable').DataTable({
        // "bLengthChange": false,
        "bInfo": false,
        "bAutoWidth": true,
        // "paging":   false,
        // "ordering": false, //排序
        // "order": [[ 2, "desc" ]],
        "info": true,//显示信息
        "columnDefs": [
            {
                orderable: false,
                targets: 0,
                "render": function (data, type, row) {
                    return '<a href=' + row[6] + '>' + data + '</a>';
                },
            },
            {
                orderable: false,
                targets: 1,
                "render": function (data, type, row) {
                    return '<a href=' + row[7] + '>' + data + '</a>';
                },
            },
            {
                orderable: false,
                targets: 1
            },
            {
                orderable: false,
                targets: 3
            },
            {
                targets: 6,
                visible: false,
                searchable: false,
            },
            {
                targets: 7,
                visible: false,
                searchable: false,
            }
        ],//第一列与第二列禁止排序
        initComplete: function () {
            var api = this.api();
            api.columns().indexes().flatten().each(function (i) {
                if (i == 4) var sel = '经验';
                else if (i == 5) var sel = '学历';
                else if (i == 3) var sel = '地址'
                else return;
                // var sel ='经验'
                var column = api.column(i);
                var select = $('<select><option value="">' + sel + '</option></select>')
                    .appendTo($(column.header()).empty())
                    .on('change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
                        column
                            .search(val ? '^' + val + '$' : '', true, false)
                            .draw();
                    });
                column.data().unique().sort().each(function (d) {
                    select.append('<option value="' + d + '">' + d + '</option>')
                });
            });
        }
    });
    $('#dataTable tbody')
        .on('mouseenter', 'td', function () {
            var colIdx = table.cell(this).index().column;

            $(table.cells().nodes()).removeClass('highlight');
            $(table.column(colIdx).nodes()).addClass('highlight');
        });
    $('input.global_filter').on('keyup click', function () {
        filterGlobal();
    });

    $('input.column_filter').on('keyup click', function () {
        filterColumn($(this).parents('tr').attr('data-column'));
    });
    showcol()
    table.columns( 3 ).search(kw,true,false).draw();
});