document.addEventListener("DOMContentLoaded", function () {
    // Function to format numbers as percentages
    function formatNumberAsPercentage(value, total) {
        return ((value / total) * 100).toFixed(2) + '%';
    }

    // Create the stock category chart
    var ctxStockCategory = document.getElementById('stockCategoryChart').getContext('2d');
    var stockCategoryChart = new Chart(ctxStockCategory, {
        type: 'bar',
        data: stockCategoryData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += context.raw || '';
                            label += ' (' + formatNumberAsPercentage(context.raw, context.chart._metasets[context.datasetIndex].total) + ')';
                            return label;
                        }
                    }
                }
            }
        }
    });

    // Create the low stock chart
    var ctxLowStock = document.getElementById('lowStockChart').getContext('2d');
    var lowStockChart = new Chart(ctxLowStock, {
        type: 'pie',
        data: lowStockData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += context.raw || '';
                            label += ' (' + formatNumberAsPercentage(context.raw, context.chart._metasets[context.datasetIndex].total) + ')';
                            return label;
                        }
                    }
                }
            }
        }
    });
});
