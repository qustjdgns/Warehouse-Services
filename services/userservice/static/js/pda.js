// URL에서 작업 모드 확인
// /pda?mode=inbound  → 입고
// /pda?mode=outbound → 출고
const params = new URLSearchParams(window.location.search);
const mode = params.get("mode");

let currentBarcode = null;

// 화면 로딩 시 작업 모드에 따라 버튼/배지 설정
window.onload = function () {
    const badge = document.getElementById("mode-badge");
    const button = document.getElementById("stock-btn");

    if (mode === "inbound") {
        badge.innerText = "입고 작업";
        button.innerText = "입고 처리";
    } else if (mode === "outbound") {
        badge.innerText = "출고 작업";
        button.innerText = "출고 처리";
    } else {
        badge.innerText = "작업 모드 없음";
        button.innerText = "처리 불가";
        button.disabled = true;
        setMessage("operator 홈에서 입고/출고 작업을 선택하세요.", "error");
    }
};

// 메시지 출력 함수
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

// QR/바코드 스캔 성공 시 실행
function onScanSuccess(decodedText) {
    currentBarcode = decodedText;

    document.getElementById("barcode").innerText = decodedText;

    fetch("/scan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            barcode: decodedText
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("product-name").innerText = "-";
            document.getElementById("stock").innerText = "-";
            document.getElementById("location").innerText = "-";
            setMessage(data.error, "error");
            return;
        }

        document.getElementById("barcode").innerText = data.barcode;
        document.getElementById("product-name").innerText = data.product.name;
        document.getElementById("stock").innerText = data.product.stock + " EA";
        document.getElementById("location").innerText = data.product.location;

        setMessage("상품 조회 완료", "success");
    })
    .catch(error => {
        setMessage("상품 조회 요청 실패: " + error, "error");
    });
}

// 입고/출고 처리
function processStock() {
    const quantity = Number(document.getElementById("quantity").value);

    if (!currentBarcode) {
        setMessage("먼저 QR/바코드를 스캔하세요.", "error");
        return;
    }

    if (quantity <= 0) {
        setMessage("수량은 1 이상이어야 합니다.", "error");
        return;
    }

    const url = mode === "inbound" ? "/stock/in" : "/stock/out";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            barcode: currentBarcode,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            setMessage(data.error, "error");

            if (data.product) {
                document.getElementById("stock").innerText = data.product.stock + " EA";
            }

            return;
        }

        document.getElementById("stock").innerText = data.product.stock + " EA";
        setMessage(data.message + " / 현재 재고: " + data.product.stock + " EA", "success");
    })
    .catch(error => {
        setMessage("재고 처리 요청 실패: " + error, "error");
    });
}

// QR 스캐너 실행
const scanner = new Html5QrcodeScanner(
    "reader",
    {
        fps: 10,
        qrbox: 240
    }
);

scanner.render(onScanSuccess);
