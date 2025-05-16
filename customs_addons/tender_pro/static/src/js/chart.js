<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        new Chart(document.getElementById('categoryChart'), {
          type: 'bar',
          data: {
            labels: ['Works', 'Goods', 'Services', 'Consultancy'],
            datasets: [{
              label: 'Count',
              data: [12, 9, 5, 3],
              backgroundColor: ['#1abc9c', '#3498db', '#f39c12', '#e74c3c'],
            }]
          },
          options: { responsive: true }
        });

        new Chart(document.getElementById('statusChart'), {
          type: 'pie',
          data: {
            labels: ['Draft', 'Active', 'Submitted', 'Won', 'Lost'],
            datasets: [{
              data: [5, 10, 8, 4, 2],
              backgroundColor: ['#95a5a6', '#2ecc71', '#f1c40f', '#27ae60', '#c0392b'],
            }]
          },
          options: { responsive: true }
        });
      });
    </script>
  </template>
</odoo>
