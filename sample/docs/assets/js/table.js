// Rotate headers helper (supports fixed columns)
function rotateHeaders(table) {
  const rotateStyle = {
    'transform': 'rotate(-90deg)',
    'transform-origin': 'bottom left',
    'vertical-align': 'bottom',
    'height': '150px',
    'white-space': 'nowrap',
    'padding': '5px',
    'text-align': 'left'
  };

  // Original table headers
  $(table.table().header()).find('th').each(function(index) {
    if (index > 1) $(this).css(rotateStyle);
  });

  // FixedColumns cloned headers
  $('.DTFC_Cloned thead th').each(function(index) {
    if (index > 1) $(this).css(rotateStyle);
  });
}

// Helper to get table data
function getTableData(table) {
  return table.rows({ search: 'applied' }).data().toArray().map(row => {
    const obj = {};
    table.columns().every(function(index) {
      const header = $(table.column(index).header()).text();
      obj[header] = row[index];
    });
    return obj;
  });
}

// Helper to get table headers
function getTableHeaders(table) {
  return table.columns().header().toArray().map(th => $(th).text());
}

// Download helper
function downloadFile(filename, content) {
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
  URL.revokeObjectURL(link.href);
}

// LaTeX export helper
function exportLaTeX(table) {
  const headers = getTableHeaders(table);
  const rows = getTableData(table);
  let latex = '\\begin{tabular}{' + 'l'.repeat(headers.length) + '}\n';
  latex += headers.join(' & ') + ' \\\\\n\\hline\n';
  rows.forEach(row => {
    latex += headers.map(h => row[h]).join(' & ') + ' \\\\\n';
  });
  latex += '\\end{tabular}';
  return latex;
}

document.addEventListener("DOMContentLoaded", function() {
  const table = $('#myTable').DataTable({
    scrollX: true,
    scrollCollapse: true,
    autoWidth: false,
    fixedColumns: { leftColumns: 2 },
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
      rotateHeaders(this.api());  // rotate headers after first render
    }
  });

  // Reapply header rotation after every redraw
  table.on('draw', function () {
    rotateHeaders(table);
  });

  // Make headers resizable and preserve rotation
  $('#myTable thead th').resizable({
    handles: 'e',
    stop: function () {
      table.columns.adjust().fixedColumns().relayout();
      rotateHeaders(table);
    }
  });
});
