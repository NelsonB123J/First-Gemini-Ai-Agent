let fileData = "";
const BACKEND_URL = "https://your-backend-name.onrender.com"; // Change this after Render deployment

// Read file content locally
document.getElementById('file-picker').addEventListener('change', (e) => {
    const reader = new FileReader();
    reader.onload = (event) => { fileData = event.target.result; };
    reader.readAsText(e.target.files[0]);
});

async function sendToAgent() {
    const input = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    
    if (!input.value) return;

    chatWindow.innerHTML += `<div class="user-msg"><b>You:</b> ${input.value}</div>`;
    
    try {
        const res = await fetch(`${BACKEND_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: input.value, fileContent: fileData })
        });
        const data = await res.json();
        chatWindow.innerHTML += `<div class="ai-msg"><b>AI:</b> ${data.response}</div>`;
    } catch (err) {
        chatWindow.innerHTML += `<div class="error">Error: Could not reach agent.</div>`;
    }
    input.value = "";
}