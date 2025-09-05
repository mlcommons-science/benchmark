// table.js

// Helper: download a file
function downloadFile(filename, text) {
  const blob = new Blob([text], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
}

// Get table headers automatically
function getTableHeaders(table) {
  const headers = [];
  table.columns().every(function() {
    headers.push($(this.header()).text().trim());
  });
  return headers;
}

// Map HTML table rows to objects keyed by headers
function getTableData(table) {
  const headers = getTableHeaders(table);
  const data = table.rows().data().toArray().map(row => {
    const obj = {};
    row.forEach((cell, i) => {
      obj[headers[i]] = cell;
    });
    return obj;
  });
  return data;
}

// Export LaTeX table
function exportLaTeX(table) {
  const headers = getTableHeaders(table);
  const data = getTableData(table);
  let latex = "\\begin{tabular}{" + "l".repeat(headers.length) + "}\\hline\n";
  latex += headers.join(" & ") + " \\\\\\hline\n";
  data.forEach(row => {
    latex += headers.map(h => row[h]).join(" & ") + " \\\\\n";
  });
  latex += "\\hline\n\\end{tabular}";
  return latex;
}

// Initialize DataTable
document.addEventListener("DOMContentLoaded", function() {
  const table = $('#myTable').DataTable({
    paging: false,
    searching: true,
    ordering: true,
    info: false,
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
    ]
  });
});
