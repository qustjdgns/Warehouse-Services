let historyData = [];

async function loadHistory() {
    const response = await fetch("/history");
    historyData = await response.json();

    renderHistory();
}

function renderHistory() {
    const keyword = document.getElementById("searchInput").value.toLowerCase();
    const typeFilter = document.getElementById("typeFilter").value;
    const tbody = document.getElementById("historyTableBody");

    tbody.innerHTML = "";

    historyData
        .filter(item => {
            const barcode = item.barcode || "";
    	    const productName = item.product_name || "";
            const worker = item.worker || "";

    	    const matchKeyword =
        	barcode.toLowerCase().includes(keyword) ||
        	productName.toLowerCase().includes(keyword) ||
        	worker.toLowerCase().includes(keyword);

    	    const matchType =
       		typeFilter === "ALL" || item.type === typeFilter;

    	    return matchKeyword && matchType;
	})

        .forEach(item => {
            const typeLabel = item.type === "IN" ? "입고" : "출고";
            const tagClass = item.type === "IN" ? "inbound" : "outbound";
            const qtyLabel = item.type === "IN"
                ? `+${item.quantity}`
                : `-${item.quantity}`;

            const row = `
                <tr>
                    <td>${item.created_at}</td>
                    <td>${item.barcode}</td>
                    <td>${item.product_name}</td>
                    <td><span class="tag ${tagClass}">${typeLabel}</span></td>
                    <td>${qtyLabel}</td>
                    <td>${item.worker}</td>
                </tr>
            `;

            tbody.innerHTML += row;
        });
}

loadHistory();
