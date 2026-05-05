console.log("JS LOADED");

// ===== Add message =====
function addMessage(text, type) {
    let chatBox = document.getElementById("chatBox");

    let div = document.createElement("div");

    // FORMAT TEXT
    let formatted = text
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")   // bold
        .replace(/\n/g, "<br>")                  // new lines
        .replace(/- /g, "• ");                   // bullets

    div.innerHTML = `<b>${type}:</b><br>${formatted}`;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}


// ===== Upload =====
document.getElementById('uploadForm').onsubmit = async function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    let res = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    let data = await res.json();

    document.getElementById('uploadStatus').innerText =
        data.message || data.error;

    addMessage("PDF uploaded.", "bot");
};


// ===== Ask =====
async function askQuestion() {
    let input = document.getElementById('query');
    let query = input.value.trim();

    if (!query) return;

    addMessage(query, "user");
    input.value = "";

    let res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
    });

    let data = await res.json();

    addMessage(data.answer || "Error", "bot");
}


// ===== Search arXiv =====
async function searchArxiv() {
    let input = document.getElementById('query');
    let query = input.value.trim();

    if (!query) {
        addMessage("Enter a topic first.", "bot");
        return;
    }

    addMessage("Searching arXiv for: " + query, "bot");

    let res = await fetch('/search_arxiv', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
    });

    let data = await res.json();

    if (!data.papers || data.papers.length === 0) {
        addMessage("No papers found.", "bot");
        return;
    }

    data.papers.forEach((p, i) => {
        let safeTitle = p.title.replace(/'/g, "");

        addMessage(
            `${i+1}. ${p.title}<br>

            <button onclick="loadPaper('${p.pdf_url}', '${safeTitle}')">
            Load Paper
            </button>

            <a href="${p.pdf_url}" target="_blank">
                <button>Download PDF</button>
            </a>
            `,
            "bot"
        );
    });
}


// ===== Load Paper =====
async function loadPaper(url, title) {
    addMessage("Loading: " + title, "bot");

    await fetch('/load_arxiv', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pdf_url: url, title: title })
    });

    addMessage("Paper loaded. Now ask your question.", "bot");
}


// ===== Events =====
document.getElementById("sendBtn").addEventListener("click", askQuestion);
document.getElementById("arxivBtn").addEventListener("click", searchArxiv);

document.getElementById("query").addEventListener("keypress", function(e) {
    if (e.key === "Enter") askQuestion();
});


formatted = formatted
    .replace(/Answer:/g, "<br><b>Answer:</b>")
    .replace(/Explanation:/g, "<br><b>Explanation:</b>")
    .replace(/Key Points:/g, "<br><b>Key Points:</b>");