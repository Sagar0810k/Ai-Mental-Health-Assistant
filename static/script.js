document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatLog = document.getElementById("chat-log");
    const chatWindow = document.getElementById("chat-window");
    const moodDisplay = document.getElementById("mood-display");

    // Function to handle form submission
    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const userMessage = chatInput.value.trim();

        if (!userMessage) return;

        // Append the user's message to the chat log
        appendMessage(userMessage, "user-message");
        chatInput.value = "";

        // Send the user's message to the server
        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                throw new Error("Failed to get a response from the server.");
            }

            const data = await response.json();
            const botReply = data.reply || "I'm here to listen.";

            // Append the bot's reply
            appendMessage(botReply, "bot-message");

            // Display mood if available
            if (data.mood) {
                moodDisplay.textContent = `Mood: ${data.mood}`;
            } else {
                moodDisplay.textContent = "Mood: Unable to detect.";
            }
        } catch (error) {
            console.error("Error:", error);
            appendMessage("Something went wrong. Please try again.", "bot-message");
            moodDisplay.textContent = "Mood: Detection error.";
        }
    });

    // Function to append messages to the chat log
    function appendMessage(message, className) {
        const messageElement = document.createElement("div");
        messageElement.className = className;
        messageElement.textContent = message;
        chatLog.appendChild(messageElement);

        // Automatically scroll to the bottom of the chat window
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});
