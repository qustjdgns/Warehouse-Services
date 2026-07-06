let inventoryData = [];

async function loadInventory() {
    const response = await fetch("/products");
    inventoryData = await response.json();

    renderInventory();
}

function getInventoryStatus(stock) {
    if (stock === 0) {
        return {
            label: "Out of Stock",
            className: "out"
        };
    }

    if (stock <= 5) {
        return {
            label: "Low Stock",
            className: "low"
        };
    }

    return {
        label: "Normal",
        className: "normal"
    };
}

function renderInventory() {
    const keyword = document.getElementById("searchInput").value.toLowerCase();
    const statusFilter = document.getElementById("statusFilter").value;
    const tbody = document.getElementById("inventoryTableBody");

    tbody.innerHTML = "";

    inventoryData
        .filter(item => {
            const status = getInventoryStatus(item.stock);

            const matchKeyword =
                item.barcode.toLowerCase().includes(keyword) ||
                item.name.toLowerCase().includes(keyword) ||
                item.location.toLowerCase().includes(keyword);

            const matchStatus =
                statusFilter === "ALL" ||
                statusFilter === status.className.toUpperCase();

            return matchKeyword && matchStatus;
        })
        .forEach((item, index) => {
            const status = getInventoryStatus(item.stock);

            const row = `
                <tr>
                    <td>${item.barcode}</td>
                    <td>${item.name}</td>
                    <td>${item.location}</td>
                    <td>${item.stock} EA</td>
                    <td>
                        <span class="status ${status.className}">
                            ${status.label}
                        </span>
                    </td>
                    <td>
                        <button class="qr-btn" onclick="openQr('${index}')">QR</button>
                    </td>
                </tr>
            `;

            tbody.innerHTML += row;
        });
}

function openQr(index) {
    const product = inventoryData[index];

    if (!product) {
        showToast("❌ Error", "상품 정보를 찾을 수 없습니다.");
        return;
    }

    openQrModal(product);
}

loadInventory();
