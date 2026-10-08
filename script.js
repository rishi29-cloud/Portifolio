const API_BASE = "http://127.0.0.1:8000/v1";
const formatNumber = new Intl.NumberFormat("en-US");
const percent = (value, digits = 1) => `${(Number(value || 0) * 100).toFixed(digits)}%`;

async function fetchJSON(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) throw new Error(`API returned ${response.status}`);
  return response.json();
}

function renderMetrics(data) {
  document.querySelector("#reels").textContent = formatNumber.format(data.reels);
  document.querySelector("#reach").textContent = formatNumber.format(data.reach);
  document.querySelector("#engagement-rate").textContent = percent(data.engagement_rate);
  document.querySelector("#follows").textContent = formatNumber.format(data.follows);
  document.querySelector("#follow-rate").textContent = `${percent(data.follow_conversion_rate, 2)} conversion rate`;
}

function renderChart(rows) {
  const chart = document.querySelector("#bar-chart");
  const maximum = Math.max(...rows.map((row) => Number(row.engagement_rate)), 0.01);
  chart.innerHTML = rows.slice(0, 8).map((row) => {
    const height = Math.max(5, (Number(row.engagement_rate) / maximum) * 100);
    return `<div class="bar-item" title="${row.dimension}: ${percent(row.engagement_rate)}">
      <span class="bar-value">${percent(row.engagement_rate)}</span>
      <div class="bar" style="height:${height}%"></div>
      <span class="bar-label">${row.dimension}</span>
    </div>`;
  }).join("");
  const leader = rows[0];
  if (leader) {
    document.querySelector("#insight-title").textContent = `${leader.dimension} leads the way.`;
    document.querySelector("#insight-copy").textContent = `This group has the highest average engagement across ${leader.reels} published Reels.`;
    document.querySelector("#insight-value").textContent = percent(leader.engagement_rate);
  }
}

function renderTable(reels) {
  document.querySelector("#reels-table").innerHTML = reels.map((reel) => `<tr>
    <td>${reel.published_date}</td><td>${reel.topic}</td><td>${Math.round(reel.duration_seconds)} sec</td>
    <td>${formatNumber.format(reel.reach)}</td><td>${formatNumber.format(reel.plays)}</td>
    <td>${percent(reel.engagement_rate)}</td><td>${percent(reel.follow_conversion_rate, 2)}</td>
  </tr>`).join("");
}

async function loadDashboard() {
  try {
    const [kpis, reels] = await Promise.all([fetchJSON("/kpis"), fetchJSON("/reels/top")]);
    renderMetrics(kpis); renderTable(reels);
    await loadBreakdown();
    document.querySelector("#api-status").classList.add("connected");
    document.querySelector("#api-status span:last-child").textContent = "Live analytics API connected";
  } catch (error) {
    document.querySelector("#api-status span:last-child").textContent = "Start the FastAPI server to load data";
    document.querySelector("#reels-table").innerHTML = `<tr><td colspan="7" class="loading">${error.message}</td></tr>`;
  }
}
async function loadBreakdown() { renderChart(await fetchJSON(`/performance/${document.querySelector("#dimension").value}`)); }
document.querySelector("#dimension").addEventListener("change", () => loadBreakdown().catch(console.error));
loadDashboard();
