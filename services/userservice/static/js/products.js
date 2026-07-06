// MariaDB + products API /  교체 예정
let products = [];

let editIndex = null;

function getStatus(stock) {
    if (stock <= 5) {
        return `<span class="status-low">Low Stock</span>`;
    }
    return `<span class="status-ok">Available</span>`;
}

function renderProducts() {
    const keyword = document.getElementById("searchInput").value.toLowerCase();
    const tbody = document.getElementById("productTableBody");

    tbody.innerHTML = "";

    products
        .filter(product =>
            product.barcode.toLowerCase().includes(keyword) ||
            product.name.toLowerCase().includes(keyword)
        )
        .forEach((product, index) => {
            const row = `
                <tr>
                    <td>${product.barcode}</td>
                    <td>${product.name}</td>
                    <td>${product.stock}</td>
                    <td>${product.location}</td>
                    <td>${getStatus(product.stock)}</td>
                    <td>
                        <button class="action-btn edit-btn" onclick="openEditModal(${index})">Edit</button>
                        <button class="action-btn delete-btn" onclick="deleteProduct(${index})">Delete</button>
                  	<button class="action-btn qr-btn" onclick="openQr('${index}')">QR</button>
		  </td>
                </tr>
            `;

            tbody.innerHTML += row;
        });
}

async function loadProducts() {
	const response = await fetch("/products");
	products = await response.json();
	renderProducts();
}


function openAddModal() {
    editIndex = null;

    document.getElementById("modalTitle").innerText = "Add Product";
    document.getElementById("barcodeInput").value = "";
    document.getElementById("nameInput").value = "";
    document.getElementById("stockInput").value = "";
    document.getElementById("locationInput").value = "";

    document.getElementById("barcodeInput").disabled = false;
    document.getElementById("productModal").style.display = "flex";
}

function openEditModal(index) {
    editIndex = index;
    const product = products[index];

    document.getElementById("modalTitle").innerText = "Edit Product";
    document.getElementById("barcodeInput").value = product.barcode;
    document.getElementById("nameInput").value = product.name;
    document.getElementById("stockInput").value = product.stock;
    document.getElementById("locationInput").value = product.location;

    // barcode는 상품 고유값이라 수정하지 못하게 함
    document.getElementById("barcodeInput").disabled = true;

    document.getElementById("productModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("productModal").style.display = "none";
}

async function saveProduct() {
    const barcode = document.getElementById("barcodeInput").value.trim();
    const name = document.getElementById("nameInput").value.trim();
    const stock = Number(document.getElementById("stockInput").value);
    const location = document.getElementById("locationInput").value.trim();

    if (!barcode || !name || stock < 0 || !location) {
        alert("모든 값을 올바르게 입력하세요.");
        return;
    }

    let url = "/products";
    let method = "POST";

    if (editIndex !== null) {
        url = "/products/" + barcode;
        method = "PUT";
    }

    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            barcode: barcode,
            name: name,
            stock: stock,
            location: location
        })
    });

    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    closeModal();

    // DB에서 다시 상품 목록 조회
    loadProducts();
}

async function deleteProduct(index) {
    const product = products[index];

    if (!confirm(`${product.name} 상품을 삭제할까요?`)) {
        return;
    }

    const response = await fetch("/products/" + product.barcode, {
        method: "DELETE"
    });

    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    // DB에서 다시 상품 목록 조회
    loadProducts();
}

function openQr(index) {
    const product = products[index];
    openQrModal(product);
}

// 페이지 로딩 시 상품 목록 표시
loadProducts();
