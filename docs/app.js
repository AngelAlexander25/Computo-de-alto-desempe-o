// Script principal para la visualización de datos de Messi
document.addEventListener('DOMContentLoaded', function() {
  const chartCtx = document.getElementById("chart").getContext("2d");
  
  // Cargar datos directamente desde el archivo JSON
  fetch("data/messi_barcelona_clean.json")
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error HTTP! Estado: ${response.status}`);
      }
      return response.text();
    })
    .then(text => {
      // Procesar el formato JSONL (cada línea es un objeto JSON separado)
      const lines = text.trim().split('\n');
      const jsonData = lines.map(line => JSON.parse(line));
      
      // Procesar los datos para la visualización
      return processData(jsonData);
    })
    .then(chartData => {
      createChart(chartData, chartCtx);
    })
    .catch(error => {
      console.error("Error cargando datos:", error);
      document.querySelector(".chart-container").innerHTML = 
        `<div class="error-message">
          <h3>Error al cargar los datos</h3>
          <p>${error.message}</p>
          <p>Ruta intentada: data/messi_barcelona_clean.json</p>
        </div>`;
    });
});

function processData(data) {
  // Filtrar solo datos de La Liga
  const laLigaData = data.filter(item => item.competition === "La Liga");
  
  // Ordenar por temporada
  laLigaData.sort((a, b) => {
    const seasonA = parseInt(a.season.split('-')[0]);
    const seasonB = parseInt(b.season.split('-')[0]);
    return seasonA - seasonB;
  });
  
  return {
    seasons: laLigaData.map(item => item.season),
    goals: laLigaData.map(item => item.goals_scored),
    assists: laLigaData.map(item => item.assists),
    minutes: laLigaData.map(item => item.minutes_played)
  };
}

function createChart(data, ctx) {
  const goalColor = 'rgba(165, 0, 68, 0.8)'; // Barça red
  const assistColor = 'rgba(0, 77, 152, 0.8)'; // Barça blue
  
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.seasons,
      datasets: [
        {
          label: "Goles",
          data: data.goals,
          backgroundColor: goalColor,
          borderColor: goalColor.replace('0.8', '1'),
          borderWidth: 1
        },
        {
          label: "Asistencias",
          data: data.assists,
          backgroundColor: assistColor,
          borderColor: assistColor.replace('0.8', '1'),
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'Rendimiento de Messi en La Liga por temporada',
          font: {
            size: 18,
            weight: 'bold'
          },
          padding: {
            top: 10,
            bottom: 20
          }
        },
        legend: {
          position: 'top'
        },
        tooltip: {
          callbacks: {
            afterLabel: function(context) {
              const index = context.dataIndex;
              const minutes = data.minutes[index];
              const datasetLabel = context.dataset.label;
              
              if (datasetLabel === "Goles") {
                const goalsPerMin = (data.goals[index] / minutes * 90).toFixed(2);
                return `Goles por 90 min: ${goalsPerMin}`;
              } else {
                const assistsPerMin = (data.assists[index] / minutes * 90).toFixed(2);
                return `Asistencias por 90 min: ${assistsPerMin}`;
              }
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Cantidad'
          },
          grid: {
            display: true,
            color: 'rgba(0, 0, 0, 0.05)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Temporada'
          },
          grid: {
            display: false
          }
        }
      }
    }
  });
}