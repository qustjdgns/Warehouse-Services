// Mock 데이터: 나중에 MariaDB API 응답으로 교체 예정

const inventoryData = {
    labels: ["Keyboard", "Mouse", "USB-C Cable", "Monitor", "Laptop Stand"],
    datasets: [{
        label: "Stock",
        data: [30, 18, 75, 12, 7]
    }]
};

const flowData = {
    labels: ["Inbound", "Outbound"],
    datasets: [{
        data: [42, 31]
    }]
};

new Chart(document.getElementById("inventoryChart"), {
    type: "bar",
    data: inventoryData
});

new Chart(document.getElementById("flowChart"), {
    type: "doughnut",
    data: flowData
});
