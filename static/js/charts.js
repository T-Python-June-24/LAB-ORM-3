let charts = {};

function updateCharts() {
  fetch("/products/api/chart-data/")
    .then((response) => response.json())
    .then((data) => {
      updateTopStats(data.top_stats);
      updateLatestProducts(data.latest_products.data);

      // Destroy existing charts before creating new ones
      Object.values(charts).forEach((chart) => chart.destroy());

      const textColor = getTextColor();
      charts.categoryDistribution = createPieChart(
        "categoryDistribution",
        "Category Distribution",
        data.category_distribution.data,
        data.category_distribution.description,
        textColor
      );
      charts.topProducts = createBarChart(
        "topProducts",
        "Top 10 Products by Quantity",
        data.top_products.data,
        data.top_products.description,
        textColor
      );
      charts.monthlySalesTrend = createLineChart(
        "monthlySalesTrend",
        "Monthly Spending Trend",
        data.monthly_sales_trend.data,
        data.monthly_sales_trend.description,
        textColor
      );
      charts.supplierDistribution = createPieChart(
        "supplierDistribution",
        "Supplier Distribution",
        data.supplier_distribution.data,
        data.supplier_distribution.description,
        textColor
      );
    });
}

function updateTopStats(stats) {
  document.getElementById("totalProducts").textContent =
    stats.total_products.toLocaleString();
  document.getElementById("totalQuantity").textContent =
    stats.total_quantity.toLocaleString();
  document.getElementById("lowStockProducts").textContent =
    stats.low_stock_products.toLocaleString();
  document.getElementById(
    "totalValue"
  ).textContent = `$${stats.total_value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
  document.getElementById("total_suppliers").textContent =
    stats.total_suppliers.toLocaleString();
}

function updateLatestProducts(products) {
  const tbody = document.getElementById("latest-products-tbody");
  tbody.innerHTML = "";
  products.forEach((product, index) => {
    const row = tbody.insertRow();
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${product.name}</td>
      <td>${product.category || "N/A"}</td>
      <td>${product.quantity.toLocaleString()}</td>
      <td>${product.supplier || "N/A"}</td>
      <td>${new Date(product.created_at).toLocaleDateString()}</td>
    `;
  });
}

function getTextColor() {
  const theme = document.documentElement.getAttribute("data-theme");
  const textColor = theme === "dark" ? "#D6D7DB" : "#272A36";

  // Update text color for all relevant elements
  document
    .querySelectorAll(".text-base-content, .stat-title, .stat-value")
    .forEach((el) => {
      el.style.color = textColor;
    });

  return textColor;
}

// Add an event listener for theme changes
document.addEventListener("DOMContentLoaded", () => {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (
        mutation.type === "attributes" &&
        mutation.attributeName === "data-theme"
      ) {
        getTextColor();
        updateCharts();
      }
    });
  });

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
});

function getChartColors(count) {
  const theme = document.documentElement.getAttribute("data-theme");
  const colors =
    theme === "dark"
      ? [
          "rgba(255, 99, 132, 0.7)",
          "rgba(54, 162, 235, 0.7)",
          "rgba(255, 206, 86, 0.7)",
          "rgba(75, 192, 192, 0.7)",
          "rgba(153, 102, 255, 0.7)",
          "rgba(255, 159, 64, 0.7)",
          "rgba(199, 199, 199, 0.7)",
          "rgba(83, 102, 255, 0.7)",
        ]
      : [
          "rgba(255, 99, 132, 0.9)",
          "rgba(54, 162, 235, 0.9)",
          "rgba(255, 206, 86, 0.9)",
          "rgba(75, 192, 192, 0.9)",
          "rgba(153, 102, 255, 0.9)",
          "rgba(255, 159, 64, 0.9)",
          "rgba(199, 199, 199, 0.9)",
          "rgba(83, 102, 255, 0.9)",
        ];
  return Array(count)
    .fill()
    .map((_, i) => colors[i % colors.length]);
}

function createPieChart(canvasId, title, data, description, textColor) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  const colors = getChartColors(Object.keys(data).length);

  const chart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: Object.keys(data),
      datasets: [
        {
          data: Object.values(data).map((item) => item.count),
          backgroundColor: colors,
          borderColor: colors.map((color) => color.replace("0.7", "1")),
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "right",
          labels: {
            font: { size: 10 },
            color: textColor,
          },
        },
        title: {
          display: true,
          text: title,
          color: textColor,
          font: { size: 16, weight: "bold" },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              let label = context.label || "";
              if (label) {
                label += ": ";
              }
              const value = data[context.label];
              label += `${value.count.toLocaleString()} (${value.percentage.toFixed(
                2
              )}%)`;
              return label;
            },
          },
        },
      },
      hover: {
        mode: "nearest",
        intersect: true,
      },
    },
  });
  document.getElementById(`${canvasId}Description`).textContent = description;
  return chart;
}

function createBarChart(canvasId, title, data, description, textColor) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  const colors = getChartColors(Object.keys(data).length);

  const chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: Object.keys(data),
      datasets: [
        {
          data: Object.values(data).map((item) => item.quantity),
          backgroundColor: colors,
          borderColor: colors.map((color) => color.replace("0.7", "1")),
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: title,
          color: textColor,
          font: { size: 16, weight: "bold" },
        },
        tooltip: {
          backgroundColor: "hsl(var(--b1))",
          titleColor: textColor,
          bodyColor: textColor,
          borderColor: textColor,
          borderWidth: 1,
          callbacks: {
            label: function (context) {
              let label = context.dataset.label || "";
              if (label) {
                label += ": ";
              }
              if (context.parsed.y !== null) {
                label += context.parsed.y.toLocaleString();
              }
              return label;
            },
          },
        },
      },
      hover: {
        mode: "nearest",
        intersect: true,
      },
      scales: {
        x: {
          ticks: {
            font: { size: 10 },
            color: textColor,
          },
        },
        y: {
          ticks: {
            font: { size: 10 },
            color: textColor,
            callback: function (value) {
              return value.toLocaleString();
            },
          },
        },
      },
    },
  });
  document.getElementById(`${canvasId}Description`).textContent = description;
  return chart;
}

function createLineChart(canvasId, title, data, description, textColor) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  const color = getChartColors(1)[0];

  const chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: Object.keys(data),
      datasets: [
        {
          data: Object.values(data),
          borderColor: color.replace("0.7", "1"),
          backgroundColor: color.replace("0.7", "0.2"),
          tension: 0.1,
          pointBackgroundColor: color,
          pointBorderColor: color.replace("0.7", "1"),
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: color.replace("0.7", "1"),
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: title,
          color: textColor,
          font: { size: 16, weight: "bold" },
        },
        tooltip: {
          backgroundColor: "hsl(var(--b1))",
          titleColor: textColor,
          bodyColor: textColor,
          borderColor: textColor,
          borderWidth: 1,
          callbacks: {
            label: function (context) {
              let label = context.dataset.label || "";
              if (label) {
                label += ": ";
              }
              if (context.parsed.y !== null) {
                label += context.parsed.y.toLocaleString();
              }
              return label;
            },
          },
        },
      },
      hover: {
        mode: "nearest",
        intersect: true,
      },
      scales: {
        x: {
          ticks: {
            font: { size: 10 },
            color: textColor,
          },
        },
        y: {
          ticks: {
            font: { size: 10 },
            color: textColor,
            callback: function (value) {
              return value.toLocaleString();
            },
          },
        },
      },
    },
  });
  document.getElementById(`${canvasId}Description`).textContent = description;
  return chart;
}

function updateChartColors(chart, textColor) {
  if (chart.options.plugins.legend) {
    chart.options.plugins.legend.labels.color = textColor;
  }
  chart.options.plugins.title.color = textColor;
  chart.options.scales.x.ticks.color = textColor;
  chart.options.scales.y.ticks.color = textColor;
  chart.update();
}

document.addEventListener("DOMContentLoaded", function () {
  updateCharts();

  // Add event listener for theme change
  document.documentElement.addEventListener("data-theme-changed", function () {
    const textColor = getTextColor();
    Object.values(charts).forEach((chart) =>
      updateChartColors(chart, textColor)
    );
  });
});
