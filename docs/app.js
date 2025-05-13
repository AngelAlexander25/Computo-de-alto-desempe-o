// New app.js that works on GitHub Pages by using local data file instead of Elasticsearch
document.addEventListener('DOMContentLoaded', function() {
  const chartCtx = document.getElementById("chart").getContext("2d");
  
  // Load data directly from the JSON file instead of Elasticsearch
  fetch("data/messi_barcelona_clean.json")
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.text();
    })
    .then(text => {
      // Parse the JSONL format (each line is a separate JSON object)
      const lines = text.trim().split('\n');
      const data = lines.map(line => JSON.parse(line));
      
      // Process the data for visualization
      return processData(data);
    })
    .then(chartData => {
      createChart(chartData, chartCtx);
    })
    .catch(error => {
      console.error("Error loading data:", error);
      document.getElementById("chart-container").innerHTML = 
        `<p>Error cargando datos: ${error.message}</p>`;
    });
});

function processData(data) {
  // Group data by season and competition
  const laLigaData = data.filter(item => item.competition === "La Liga");
  
  // Sort by season
  laLigaData.sort((a, b) => {
    const seasonA = parseInt(a.season.split('-')[0]);
    const seasonB = parseInt(b.season.split('-')[0]);
    return seasonA - seasonB;
  });
  
  return {
    seasons: laLigaData.map(item => item.season),
    goals: laLigaData.map(item => item.goals_scored),
    assists: laLigaData.map(item => item.assists)
  };
}

function createChart(data, ctx) {
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.seasons,
      datasets: [
        {
          label: "Goles por temporada",
          data: data.goals,
          backgroundColor: "rgba(255, 99, 132, 0.7)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1
        },
        {
          label: "Asistencias por temporada",
          data: data.assists,
          backgroundColor: "rgba(54, 162, 235, 0.7)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Estadísticas de Messi en La Liga por temporada',
          font: {
            size: 16
          }
        },
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Cantidad'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Temporada'
          }
        }
      }
    }
  });
}