const chartCtx = document.getElementById("chart").getContext("2d");

fetch("http://localhost:9200/messi_barcelona/_search?size=100", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    query: { match_all: {} },
    sort: [{ season: "asc" }]
  })
})
.then(res => res.json())
.then(data => {
  const hits = data.hits.hits.map(hit => hit._source);
  const seasons = hits.map(d => d.season);
  const goals = hits.map(d => d.goals_scored);

  new Chart(chartCtx, {
    type: "bar",
    data: {
      labels: seasons,
      datasets: [{
        label: "Goles por temporada",
        data: goals,
        backgroundColor: "rgba(54, 162, 235, 0.5)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1
      }]
    }
  });
});
