# Sample Table with DataTables

This table supports **sorting, searching, column visibility, and exporting** thanks to [DataTables](https://datatables.net/).

<div class="datatable-wrapper">
  <table id="myTable" class="display" style="width:100%">
    <thead>
      <tr>
        <th>Name</th>
        <th>Role</th>
        <th>Location</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Alice</td><td>Engineer</td><td>New York</td></tr>
      <tr><td>Bob</td><td>Designer</td><td>San Francisco</td></tr>
      <tr><td>Charlie</td><td>Manager</td><td>London</td></tr>
      <tr><td>Dana</td><td>Analyst</td><td>Berlin</td></tr>
      <tr><td>Eve</td><td>Engineer</td><td>Tokyo</td></tr>
      <tr><td>Frank</td><td>Designer</td><td>Toronto</td></tr>
    </tbody>
  </table>
</div>

<!-- DataTables Buttons extension -->
<script src="https://cdn.datatables.net/buttons/2.4.1/js/dataTables.buttons.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.4.1/js/buttons.html5.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/buttons/2.4.1/css/buttons.dataTables.min.css" />

<script type="text/javascript">
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

  document.addEventListener("DOMContentLoaded", function() {
    const table = $('#myTable').DataTable({
      paging: false,   // show all rows
      searching: true, // keep search box
      ordering: true,  // enable sorting
      info: false,     // remove "Showing X of Y entries"
      dom: 'Bfrtip',   // show buttons toolbar
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
</script>
