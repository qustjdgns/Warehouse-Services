document.addEventListener("DOMContentLoaded", function () {
    loadProfile();
});

async function loadProfile() {
    const response = await fetch("/settings/me");
    const data = await response.json();

    if (data.error) {
        showToast("⚠ Warning", data.error);
        return;
    }

    document.getElementById("profile-username").innerText = data.username;
    document.getElementById("profile-role").innerText = data.role;
    document.getElementById("fullNameInput").value = data.full_name;

    // 상단/사이드바 표시도 최신화
    localStorage.setItem("full_name", data.full_name);
    localStorage.setItem("role", data.role);
}

async function updateProfile() {
    const fullName = document.getElementById("fullNameInput").value.trim();

    if (!fullName) {
        showToast("⚠ Warning", "Full Name을 입력하세요.");
        return;
    }

    const response = await fetch("/settings/profile", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            full_name: fullName
        })
    });

    const data = await response.json();

    if (data.error) {
        showToast("⚠ Warning", data.error);
        return;
    }

    localStorage.setItem("full_name", data.full_name);

    const currentUser = document.getElementById("current-user");
    const sidebarFullName = document.getElementById("sidebar-full-name");

    if (currentUser) {
        currentUser.innerText = data.full_name;
    }

    if (sidebarFullName) {
        sidebarFullName.innerText = data.full_name;
    }

    showToast("✅ Profile Updated", data.full_name);
}

async function updatePassword() {
    const currentPassword = document.getElementById("currentPasswordInput").value.trim();
    const newPassword = document.getElementById("newPasswordInput").value.trim();

    if (!currentPassword || !newPassword) {
        showToast("⚠ Warning", "현재 비밀번호와 새 비밀번호를 입력하세요.");
        return;
    }

    const response = await fetch("/settings/password", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            current_password: currentPassword,
            new_password: newPassword
        })
    });

    const data = await response.json();

    if (data.error) {
        showToast("⚠ Warning", data.error);
        return;
    }

    document.getElementById("currentPasswordInput").value = "";
    document.getElementById("newPasswordInput").value = "";

    showToast("✅ Password Updated", "비밀번호가 변경되었습니다.");
}

async function deleteAccount() {
    if (!confirm("정말 회원 탈퇴하시겠습니까? 이 작업은 되돌릴 수 없습니다.")) {
        return;
    }

    const response = await fetch("/settings/account", {
        method: "DELETE"
    });

    const data = await response.json();

    if (data.error) {
        showToast("⚠ Warning", data.error);
        return;
    }

    localStorage.clear();

    alert("회원 탈퇴가 완료되었습니다.");
    window.location.href = "/login-page";
}
