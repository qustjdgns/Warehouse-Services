let users = [];
let editUserId = null;

async function loadUsers() {
    const response = await fetch("/users");
    users = await response.json();
    renderUsers();
}

function getRoleBadge(role) {
    if (role === "manager") {
        return `<span class="role-badge role-manager">Manager</span>`;
    }

    return `<span class="role-badge role-operator">Operator</span>`;
}

function renderUsers() {
    const keyword = document.getElementById("searchInput").value.toLowerCase();
    const roleFilter = document.getElementById("roleFilter").value;
    const tbody = document.getElementById("usersTableBody");

    tbody.innerHTML = "";

    users
        .filter(user => {
            const matchKeyword =
                user.username.toLowerCase().includes(keyword) ||
                user.full_name.toLowerCase().includes(keyword);

            const matchRole =
                roleFilter === "ALL" || user.role === roleFilter;

            return matchKeyword && matchRole;
        })
        .forEach(user => {
            const row = `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.full_name}</td>
                    <td>${getRoleBadge(user.role)}</td>
                    <td>
                        <button class="action-btn edit-btn" onclick="openEditUserModal(${user.id})">Edit</button>
                        <button class="action-btn delete-btn" onclick="deleteUser(${user.id})">Delete</button>
                    </td>
                </tr>
            `;

            tbody.innerHTML += row;
        });
}

function openAddUserModal() {
    editUserId = null;

    document.getElementById("modalTitle").innerText = "Add User";
    document.getElementById("usernameInput").value = "";
    document.getElementById("fullNameInput").value = "";
    document.getElementById("passwordInput").value = "";
    document.getElementById("roleInput").value = "operator";

    document.getElementById("usernameInput").disabled = false;
    document.getElementById("passwordInput").placeholder = "Password";

    document.getElementById("userModal").style.display = "flex";
}

function openEditUserModal(userId) {
    editUserId = userId;

    const user = users.find(item => item.id === userId);

    if (!user) {
        showToast("❌ Error", "사용자를 찾을 수 없습니다.");
        return;
    }

    document.getElementById("modalTitle").innerText = "Edit User";
    document.getElementById("usernameInput").value = user.username;
    document.getElementById("fullNameInput").value = user.full_name;
    document.getElementById("passwordInput").value = "";
    document.getElementById("roleInput").value = user.role;

    document.getElementById("usernameInput").disabled = true;
    document.getElementById("passwordInput").placeholder = "변경하지 않으려면 비워두세요";

    document.getElementById("userModal").style.display = "flex";
}

function closeUserModal() {
    document.getElementById("userModal").style.display = "none";
}

async function saveUser() {
    const username = document.getElementById("usernameInput").value.trim();
    const fullName = document.getElementById("fullNameInput").value.trim();
    const password = document.getElementById("passwordInput").value.trim();
    const role = document.getElementById("roleInput").value;

    if (!username || !fullName || !role) {
        showToast("⚠ Warning", "Username, Full Name, Role은 필수입니다.");
        return;
    }

    if (editUserId === null && !password) {
        showToast("⚠ Warning", "신규 사용자는 Password가 필요합니다.");
        return;
    }

    const isEditMode = editUserId !== null;

    let url = "/users";
    let method = "POST";

    if (isEditMode) {
        url = "/users/" + editUserId;
        method = "PUT";
    }

    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            full_name: fullName,
            password: password,
            role: role
        })
    });

    const data = await response.json();

    if (data.error) {
        showToast("⚠ Warning", data.error);
        return;
    }

    closeUserModal();
    await loadUsers();

    if (isEditMode) {
        showToast("✏ User Updated", fullName);
    } else {
        showToast("✅ User Added", fullName);
    }
}

async function deleteUser(userId) {
    const user = users.find(item => item.id === userId);

    if (!user) {
        showToast("❌ Error", "사용자를 찾을 수 없습니다.");
        return;
    }

    const currentUser = localStorage.getItem("username");

    if (user.username === currentUser) {
        showToast("⚠ Warning", "현재 로그인한 계정은 삭제할 수 없습니다.");
        return;
    }

    if (!confirm(`${user.full_name} 사용자를 삭제할까요?`)) {
        return;
    }

    const response = await fetch("/users/" + userId, {
        method: "DELETE"
    });

    const data = await response.json();

    if (data.error) {
        showToast("⚠ Warning", data.error);
        return;
    }

    await loadUsers();

    showToast("🗑 User Deleted", user.full_name);
}

loadUsers();
