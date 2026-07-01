// static/js/base.js

document.addEventListener("DOMContentLoaded", function () {

    // 로그인한 사용자 표시
    const username = localStorage.getItem("username");

    const currentUser = document.getElementById("current-user");

    if (username && currentUser) {
        currentUser.innerText = username;
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
