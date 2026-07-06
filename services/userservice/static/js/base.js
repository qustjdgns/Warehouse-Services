// static/js/base.js

document.addEventListener("DOMContentLoaded", function () {

    // 로그인한 사용자 표시
    const username = localStorage.getItem("username");
    const fullName = localStorage.getItem("full_name");
    const role = localStorage.getItem("role");

    const currentUser = document.getElementById("current-user");
    const sidebarFullName = document.getElementById("sidebar-full-name");
    const sidebarRole = document.getElementById("sidebar-role");

    if (currentUser) {
	currentUser.innerText = fullName || username || "Guest";
    }

    if (sidebarFullName) {
	sidebarFullName.innerText = fullName || username || "Guest";
    }

    if (sidebarRole) {
	sidebarRole.innerText = role || "-";
    }
    
    // 로그인 후 Welcome Toast 표시
    const toastData = localStorage.getItem("toast");

    if (toastData) {

        const toast = JSON.parse(toastData);

        showToast(
            toast.title,
            toast.message
        );

        localStorage.removeItem("toast");
    }

});

function showToast(title, message) {

    const toast = document.getElementById("toast");

    if (!toast) return;

    toast.innerHTML = `
    	<strong style="font-size:22px;">
        	${title}
   	</strong>
    	<br>
    	<span style="font-size:18px;">
        	${message}
    	</span>
    `;

    toast.classList.add("show");

    setTimeout(() => {

        toast.classList.remove("show");

    }, 3000);

}

function applyTheme() {
    const theme = localStorage.getItem("theme") || "light";

    if (theme === "dark") {
        document.body.classList.add("dark-mode");
    } else {
        document.body.classList.remove("dark-mode");
    }

    const toggle = document.getElementById("themeToggle");

    if (toggle) {
        toggle.checked = theme === "dark";
    }
}

function toggleTheme() {
    const toggle = document.getElementById("themeToggle");
    const isDark = toggle.checked;

    if (isDark) {
        localStorage.setItem("theme", "dark");
        document.body.classList.add("dark-mode");
        showToast("🌙 Dark Mode", "Dark mode enabled");
    } else {
        localStorage.setItem("theme", "light");
        document.body.classList.remove("dark-mode");
        showToast("☀ Light Mode", "Light mode enabled");
    }
}

applyTheme();

function logout() {

    fetch("/logout", {
        method: "POST"
    })
    .then(() => {

        localStorage.removeItem("username");
        localStorage.removeItem("role");
        localStorage.removeItem("toast");

        window.location.href = "/login-page";

    });

}

async function loadNotifications() {
    const response = await fetch("/notifications");
    const notifications = await response.json();

    const countEl = document.getElementById("notification-count");
    const listEl = document.getElementById("notification-list");

    if (!countEl || !listEl) return;

    listEl.innerHTML = "";

    if (notifications.length > 0) {
        countEl.innerText = notifications.length;
        countEl.style.display = "inline-block";
    } else {
        countEl.style.display = "none";
        listEl.innerHTML = `
            <div class="notification-item">
                <strong>알림 없음</strong>
                <p>현재 확인할 알림이 없습니다.</p>
            </div>
        `;
        return;
    }

    notifications.forEach(item => {
        const icon = item.type === "warning" ? "⚠" : "📦";
        const className = item.type === "warning"
            ? "notification-warning"
            : "notification-info";

        listEl.innerHTML += `
            <div class="notification-item ${className}">
                <strong>${icon} ${item.title}</strong>
                <p>${item.message}</p>
            </div>
        `;
    });
}

function toggleNotifications() {
    const panel = document.getElementById("notification-panel");

    if (!panel) return;

    panel.classList.toggle("show");

    loadNotifications();
}

document.addEventListener("click", function (event) {
    const wrapper = document.querySelector(".notification-wrapper");

    if (!wrapper) return;

    if (!wrapper.contains(event.target)) {
        const panel = document.getElementById("notification-panel");

        if (panel) {
            panel.classList.remove("show");
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    loadNotifications();
});

let currentQrBarcode = null;

function openQrModal(product) {
    currentQrBarcode = product.barcode;

    const qrUrl = `/products/${product.barcode}/qrcode`;

    document.getElementById("qrImage").src = qrUrl;
    document.getElementById("qrProductName").innerText = product.name;
    document.getElementById("qrBarcode").innerText = product.barcode;
    document.getElementById("qrLocation").innerText = product.location;
    document.getElementById("qrStock").innerText = product.stock + " EA";

    const downloadLink = document.getElementById("qrDownloadLink");
    downloadLink.href = qrUrl;
    downloadLink.download = `${product.barcode}.png`;

    document.getElementById("qrModal").classList.add("show");
}

function closeQrModal() {
    document.getElementById("qrModal").classList.remove("show");
}

function copyBarcode() {
    navigator.clipboard.writeText(currentQrBarcode);

    showToast(
        "📋 Copied",
        currentQrBarcode + " 복사 완료"
    );
}

function printQr() {
    window.print();
}

document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeQrModal();
    }
});
