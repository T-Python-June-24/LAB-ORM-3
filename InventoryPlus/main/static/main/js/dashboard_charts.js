document.addEventListener("DOMContentLoaded", function () {
    // Function to format numbers as percentages
    function formatNumberAsPercentage(value, total) {
        return ((value / total) * 100).toFixed(2) + '%';
    }

    // Function to create the stock category chart
    function createStockCategoryChart(data) {
        var ctxStockCategory = document.getElementById('stockCategoryChart').getContext('2d');
        var stockCategoryChart = new Chart(ctxStockCategory, {
            type: 'bar',
            data: data,
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
                },
                onClick: function (event, elements) {
                    if (elements.length > 0) {
                        var index = elements[0].index;
                        var categoryName = data.labels[index];
                        fetchCategoryDetails(categoryName);
                    }
                }
            }
        });
    }

    // Function to fetch category details
    function fetchCategoryDetails(categoryName) {
        fetch(`/analytics/category-details/?category=${categoryName}`)
            .then(response => response.json())
            .then(data => {
                updateCategoryDetailsChart(data);
            });
    }

    // Function to update the category details chart
    function updateCategoryDetailsChart(data) {
        var ctxCategoryDetails = document.getElementById('categoryDetailsChart').getContext('2d');
        new Chart(ctxCategoryDetails, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Stock Levels',
                    data: data.data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
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
    }

    // Data for the initial stock category chart
    var stockCategoryData = {
        labels: stockCategoryLabels,
        datasets: [{
            label: 'Total Stock',
            data: stockCategoryData,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    };

    // Create the initial stock category chart
    createStockCategoryChart(stockCategoryData);

    // Create the low stock chart
    var ctxLowStock = document.getElementById('lowStockChart').getContext('2d');
    var lowStockChart = new Chart(ctxLowStock, {
        type: 'pie',
        data: {
            labels: lowStockLabels,
            datasets: [{
                data: lowStockData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
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
