const API_ENDPOINT = "/predict";

document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const imagePreview = document.getElementById("image-preview");
    const fileInput = document.getElementById("fileInput");
    const fileLabel = document.getElementById("fileLabel");
    const checkButton = document.getElementById("checkButton");
    const aiProbElement = document.getElementById('ai-probability');
    const resultMessage = document.getElementById('result-message');

    handleFileInput();

    // フォーム送信時処理
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        submitForm(form);
    });

    // ファイル選択処理
    fileInput.addEventListener("change", function(e) {
        resetResults();

        const file = e.target.files[0];
        const reader = new FileReader();

        reader.onloadend = function() {
            imagePreview.style.backgroundImage = 'url(' + reader.result + ')';
            let fileName = file.name;
            if (fileName.length > 30) {
                fileName = fileName.slice(0, 30) + "...";
            }
            fileLabel.textContent = fileName;
        }

        if (file) {
            reader.readAsDataURL(file);
        } else {
            fileLabel.textContent = "画像ファイルを選択してください";
        }

        handleFileInput();
    });
});

// ファイルの有無に応じてCHECKボタンの状態を制御
function handleFileInput() {
    const fileInput = document.getElementById('fileInput');
    const checkButton = document.getElementById('checkButton');

    if (fileInput.files && fileInput.files[0]) {
        checkButton.disabled = false;
        checkButton.style.backgroundColor = "black";
    } else {
        checkButton.disabled = true;
        checkButton.style.backgroundColor = "grey";
    }
}

// 判定結果をリセット
function resetResults() {
    document.getElementById('ai-probability').textContent = '';
    document.getElementById('result-message').textContent = '';
    document.getElementById('image-preview').style.backgroundImage = '';
}

// フォームデータをAPIへ送信し結果表示
function submitForm(form) {
    const formData = new FormData(form);
    const loadingOverlay = document.getElementById("loading-overlay");

    loadingOverlay.style.display = "flex"; 

    fetch(API_ENDPOINT, {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loadingOverlay.style.display = "none"; 

        document.getElementById('ai-probability').textContent = data.AI_probability;

        let messageElement = document.getElementById('result-message');
        if (data.AI_probability >= 60) {
            messageElement.textContent = "このイラストはAIによって作成された可能性が高いです!!";
            messageElement.style.color = "red";
        } else if (data.AI_probability >= 40) {
            messageElement.textContent = "このイラストは判定が難しいです。";
            messageElement.style.color = "orange";
        } else {
            messageElement.textContent = "このイラストはAIによって作成された可能性が低いです!!";
            messageElement.style.color = "blue";
        }

        // ai-probability部分が画面の中央に来るようにスクロール
        scrollToCenter(document.getElementById('ai-probability'));
    })
    .catch(error => {
        loadingOverlay.style.display = "none"; 
        console.error("Error:", error);
        alert("Error occurred during prediction.");
    });
}

// 画面中央に要素を表示するスクロール機能
function scrollToCenter(element) {
    let elementRect = element.getBoundingClientRect();
    let absoluteElementTop = elementRect.top + window.pageYOffset;
    let middlePosition = absoluteElementTop - (window.innerHeight / 2);
    window.scrollTo({top: middlePosition, behavior: 'smooth'});
}