// script.js

function sendMessage() {
    var userMessage = document.getElementById("user-message").value;
    if (userMessage.trim() !== "") {
        appendMessage("user", userMessage);
        document.getElementById("user-message").value = "";

        // Send user message to server
        fetch("/get_response", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "user_message=" + encodeURIComponent(userMessage),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Bot Response:", data.response); // Add this line for debugging
            appendMessage("bot", data.response);
        });
    }
}

// Function to clear chat history on the client side
function clearHistory() {
    document.getElementById("chat-box").innerHTML = "";
}

document.getElementById("user-message").addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function appendMessage(sender, message) {
    var chatBox = document.getElementById("chat-box");
    var messageDiv = document.createElement("div");
    messageDiv.className = sender;
    messageDiv.innerHTML = `<strong>${sender.charAt(0).toUpperCase() + sender.slice(1)}:</strong> ${message}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
