document.addEventListener("DOMContentLoaded", function () {
    const username = localStorage.getItem("username");
    const fullName = localStorage.getItem("full_name");
    const role = localStorage.getItem("role");

    const nameEl = document.getElementById("operator-full-name");
    const roleEl = document.getElementById("operator-role");

    if (nameEl) {
        nameEl.innerText = fullName || username || "Guest";
    }

    if (roleEl) {
        roleEl.innerText = role || "-";
    }

    const todayEl = document.getElementById("operator-today");
    if (todayEl) {
        const today = new Date().toISOString().slice(0, 10);
        todayEl.innerText = today;
    }

    const toastData = localStorage.getItem("toast");

    if (toastData) {
        const toast = JSON.parse(toastData);
        showOperatorToast(toast.title, toast.message);
        localStorage.removeItem("toast");
    }
    loadOperatorSummary();
    loadOperatorRecentHistory();
});

async function loadOperatorSummary() {
    const response = await fetch("/dashboard/summary");
    const data = await response.json();

    const inboundEl = document.getElementById("operator-inbound-count");
    const outboundEl = document.getElementById("operator-outbound-count");

    if (inboundEl) {
        inboundEl.innerHTML = `${data.today_inbound} <span>건</span>`;
    }

    if (outboundEl) {
        outboundEl.innerHTML = `${data.today_outbound} <span>건</span>`;
    }
}

async function loadOperatorRecentHistory() {
    const response = await fetch("/dashboard/recent-history");
    const data = await response.json();

    const historyBox = document.getElementById("operator-recent-history");

    if (!historyBox) {
        return;
    }

    historyBox.innerHTML = "";

    data.slice(0, 3).forEach(item => {
        const typeLabel = item.type === "IN" ? "입고" : "출고";
        const tagClass = item.type === "IN" ? "inbound-tag" : "outbound-tag";
        const qtyLabel = item.type === "IN"
            ? `${item.quantity} EA`
            : `${item.quantity} EA`;

        const row = `
            <div class="history-row">
                <div>
                    <strong>${item.barcode}</strong>
                    <p>${item.product_name}</p>
                    <p class="history-meta">${item.worker || "-"} · ${item.time}</p>
		</div>
                <span class="tag ${tagClass}">${typeLabel}</span>
                <span>${qtyLabel}</span>
            </div>
        `;

        historyBox.innerHTML += row;
    });

    if (data.length === 0) {
        historyBox.innerHTML = `
            <div class="empty-history">
                최근 작업 내역이 없습니다.
            </div>
        `;
    }
}

function showOperatorToast(title, message) {
    const toast = document.getElementById("operator-toast");

    if (!toast) return;

    toast.innerHTML = `
        <strong>${title}</strong><br>
        <span>${message}</span>
    `;

    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}
