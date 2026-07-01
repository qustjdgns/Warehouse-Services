let inventoryChart = null;
let flowChart = null;

async function loadSummary() {
    const response = await fetch("/dashboard/summary");
    const data = await response.json();

    document.getElementById("total-products").innerText = data.total_products;
    document.getElementById("today-inbound").innerText = data.today_inbound;
    document.getElementById("today-outbound").innerText = data.today_outbound;
    document.getElementById("low-stock").innerText = data.low_stock;

    renderFlowChart(data.today_inbound, data.today_outbound);
}

async function loadInventoryChart() {
    const response = await fetch("/dashboard/inventory-chart");
    const data = await response.json();

    const labels = data.map(item => item.name);
    const stocks = data.map(item => item.stock);

    renderInventoryChart(labels, stocks);
}

async function loadRecentHistory() {
    const response = await fetch("/dashboard/recent-history");
    const data = await response.json();

    const tbody = document.getElementById("recent-history-body");
    tbody.innerHTML = "";

    data.forEach(item => {
        const typeLabel = item.type === "IN" ? "Inbound" : "Outbound";
        const qtyLabel = item.type === "IN" ? `+${item.quantity}` : `-${item.quantity}`;
        const tagClass = item.type === "IN" ? "inbound" : "outbound";

        tbody.innerHTML += `
            <tr>
                <td>${item.barcode}</td>
                <td>${item.product_name}</td>
                <td><span class="tag ${tagClass}">${typeLabel}</span></td>
                <td>${qtyLabel}</td>
                <td>${item.time}</td>
            </tr>
        `;
    });
}

async function loadLowStock() {
    const response = await fetch("/dashboard/low-stock");
    const data = await response.json();

    const list = document.getElementById("low-stock-list");
    list.innerHTML = "";

    data.forEach(item => {
        list.innerHTML += `
            <div class="low-stock-item">
                <div>
                    <strong>${item.name}</strong>
                    <p>${item.barcode} · ${item.location}</p>
                </div>
                <span class="low-count">${item.stock} EA</span>
            </div>
        `;
    });
}

function renderInventoryChart(labels, stocks) {
    const ctx = document.getElementById("inventoryChart");

    if (inventoryChart !== null) {
        inventoryChart.destroy();
    }

    inventoryChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Stock",
                data: stocks
            }]
        }
    });
}

function renderFlowChart(inbound, outbound) {
    const ctx = document.getElementById("flowChart");

    if (flowChart !== null) {
        flowChart.destroy();
    }

    flowChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Inbound", "Outbound"],
            datasets: [{
                data: [inbound, outbound]
            }]
        }
    });
}

async function loadDashboard() {
    await loadSummary();
    await loadInventoryChart();
    await loadRecentHistory();
    await loadLowStock();
}

loadDashboard();
