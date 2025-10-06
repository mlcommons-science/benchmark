// Rotate headers helper
function rotateHeaders(table) {
  $(table.table().header()).find('th').each(function(index) {
    if (index > 1) { // skip first two columns
      $(this).css({
        'transform': 'rotate(-90deg)',
        'transform-origin': 'bottom left',
        'vertical-align': 'bottom',
        'height': '150px',
        'white-space': 'nowrap',
        'padding': '5px',
        'text-align': 'left'
      });
    }
  });
}

document.addEventListener("DOMContentLoaded", function() {
  const table = $('#myTable').DataTable({
    scrollX: true,
    scrollCollapse: true,
    autoWidth: false,
    fixedColumns: {
      leftColumns: 2
    },
    paging: false,
    searching: true,
    ordering: true,
    info: false,
    colReorder: true,
    dom: 'Bfrtip',
    buttons: [
      { extend: 'colvis', text: 'Toggle Columns' },
      {
        text: 'Export JSON',
        action: function () {
          const data = getTableData(table);
          downloadFile('table.json', JSON.stringify(data, null, 2));
        }
      },
      {
        text: 'Export CSV',
        action: function () {
          const data = getTableData(table);
          const headers = getTableHeaders(table);
          const csv = [headers.join(",")].concat(
            data.map(row => headers.map(h => row[h]).join(","))
          );
          downloadFile('table.csv', csv.join("\n"));
        }
      },
      {
        text: 'Export YAML',
        action: function () {
          const data = getTableData(table);
          downloadFile('table.yaml', jsyaml.dump(data));
        }
      },
      {
        text: 'Export LaTeX',
        action: function () {
          downloadFile('table.tex', exportLaTeX(table));
        }
      }
    ],
    initComplete: function () {
      rotateHeaders(this.api());  // rotate after first render
    }
  });

  // Reapply header rotation after every redraw
  table.on('draw', function () {
    rotateHeaders(table);
  });

  // Keep resizable working
  $('#myTable thead th').resizable({
    handles: 'e',
    stop: function () {
      table.columns.adjust().fixedColumns().relayout();
      rotateHeaders(table); // ensure rotation persists after resize
    }
  });
});
