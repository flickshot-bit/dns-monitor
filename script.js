let prevChanges = 0;
let changesHistory = [];
let changesChart, typesChart;

setInterval(function() {
    document.getElementById('clock').textContent = new Date().toLocaleTimeString();
}, 1000);
document.getElementById('clock').textContent = new Date().toLocaleTimeString();

function typeBadge(type) {
    var colors = { 'A': 'badge-info', 'MX': 'badge-success', 'NS': 'badge-warning', 'CNAME': 'badge-error' };
    return '<span class="badge badge-outline badge-xs ' + (colors[type] || 'badge-ghost') + '">' + type + '</span>';
}

changesChart = new Chart(document.getElementById('changesChart'), {
    type: 'line',
    data: { labels: [], datasets: [{ data: [], borderColor: '#00e5ff', backgroundColor: 'rgba(0,229,255,0.08)', tension: 0.4, fill: true, pointRadius: 4, pointBackgroundColor: '#00e5ff', borderWidth: 2 }] },
    options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#555', font: { size: 9 } }, grid: { color: '#222' } }, y: { ticks: { color: '#555', font: { size: 9 } }, grid: { color: '#222' }, beginAtZero: true } } }
});

typesChart = new Chart(document.getElementById('typesChart'), {
    type: 'doughnut',
    data: { labels: ['A', 'MX', 'NS', 'CNAME'], datasets: [{ data: [0,0,0,0], backgroundColor: ['#00bcd4','#4caf50','#ce93d8','#ff9800'], borderColor: '#1d232a', borderWidth: 3 }] },
    options: { responsive: true, cutout: '60%', plugins: { legend: { position: 'right', labels: { color: '#888', font: { size: 11 }, padding: 12, boxWidth: 12 } } } }
});

function updateCharts(data) {
    var now = new Date().toLocaleTimeString();
    changesHistory.push({ time: now, val: data.total_changes });
    if (changesHistory.length > 12) changesHistory.shift();
    changesChart.data.labels = changesHistory.map(function(h) { return h.time; });
    changesChart.data.datasets[0].data = changesHistory.map(function(h) { return h.val; });
    changesChart.update('none');
    var counts = { A: 0, MX: 0, NS: 0, CNAME: 0 };
    data.records.forEach(function(r) { if (counts[r.record_type] !== undefined) counts[r.record_type]++; });
    typesChart.data.datasets[0].data = Object.values(counts);
    typesChart.update('none');
}

function fetchData() {
    fetch('/api/data')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            document.getElementById('total-checks').textContent = data.total_checks;
            document.getElementById('total-changes').textContent = data.total_changes;
            document.getElementById('changes-count').textContent = data.changes.length;
            document.getElementById('records-count').textContent = data.records.length;
            prevChanges = data.total_changes;
            var cb = document.getElementById('changes-body');
            if (data.changes.length === 0) {
                cb.innerHTML = '<tr><td colspan="4" class="text-center opacity-30 py-6">No changes yet</td></tr>';
            } else {
                cb.innerHTML = data.changes.map(function(c) {
                    return '<tr><td class="text-red-400 font-bold">' + c.domain + '</td><td>' + typeBadge(c.record_type) + '</td><td class="text-red-400">' + c.new_value + '</td><td class="opacity-40">' + c.detected_at + '</td></tr>';
                }).join('');
            }
            document.getElementById('records-body').innerHTML = data.records.map(function(r) {
                return '<tr><td class="font-bold">' + r.domain + '</td><td>' + typeBadge(r.record_type) + '</td><td class="opacity-60">' + r.value + '</td><td class="opacity-40">' + r.timestamp + '</td></tr>';
            }).join('');
            updateCharts(data);
        })
        .catch(function(err) { console.error('Error:', err); });
}

fetchData();
setInterval(fetchData, 10000);
