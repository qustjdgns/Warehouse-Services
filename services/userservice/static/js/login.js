function setMessage(text, type) {
    const message = document.getElementById("message");

    message.innerText = text;
    message.className = "message";

    if (type === "success") {
        message.classList.add("success");
    }

    if (type === "error") {
        message.classList.add("error");
    }
}

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (!username || !password) {
        setMessage("ID와 Password를 입력하세요.", "error");
        return;
    }

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            setMessage(data.error, "error");
            return;
        }

        setMessage("로그인 성공", "success");

        setTimeout(() => {
            if (data.role === "operator") {
                window.location.href = "/operator/home";
            } else if (data.role === "manager") {
                window.location.href = "/manager/dashboard";
            }
        }, 500);
    })
    .catch(error => {
        setMessage("로그인 요청 실패: " + error, "error");
    });
}
