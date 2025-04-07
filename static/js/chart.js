function drawDonutChart(score) {
    const ctx = document.getElementById('donutChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Match %', 'Remaining %'],
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: ['#28a745', '#e0e0e0']
            }]
        },
        options: {
            cutout: '70%',
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

