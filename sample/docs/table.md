# Sample Table with DataTables

This table supports **sorting, searching, and pagination** thanks to [DataTables](https://datatables.net/).

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

<script type="text/javascript">
  document.addEventListener("DOMContentLoaded", function() {
    $('#myTable').DataTable({
      paging: true,
      searching: true,
      ordering: true,
      order: [[0, 'asc']] // sort first column by default
    });
  });
</script>
