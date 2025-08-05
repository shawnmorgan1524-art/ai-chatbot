/* Front‑end logic for the AI chat interface.
 *
 * This script defines the behaviour of the chat interface. Users can send a
 * message by pressing the Send button or hitting Enter. The message is
 * appended to the chat window and sent to the backend via fetch API. The
 * backend response is displayed as an assistant message.
 */

const API_URL = "http://localhost:8000/chat"; // Update this when deploying

/**
 * Append a message to the chat window.
 *
 * @param {string} content - The text content of the message.
 * @param {string} role - Either "user" or "assistant".
 */
function appendMessage(content, role) {
  const messagesDiv = document.getElementById("messages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${role}`;

  const bubbleDiv = document.createElement("div");
  bubbleDiv.className = "bubble";
  bubbleDiv.textContent = content;

  messageDiv.appendChild(bubbleDiv);
  messagesDiv.appendChild(messageDiv);

  // Scroll to the bottom of the messages div
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

/**
 * Send the user's message to the backend and display the assistant's reply.
 */
async function sendMessage() {
  const input = document.getElementById("userInput");
  const text = input.value.trim();
  if (!text) {
    return; // Do nothing if the input is empty
  }

  // Display the user's message
  appendMessage(text, "user");
  input.value = "";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: text }),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Error connecting to server.");
    }
    const data = await response.json();
    appendMessage(data.reply, "assistant");
  } catch (error) {
    console.error(error);
    appendMessage(
      "Sorry, there was an error. Please try again later.",
      "assistant"
    );
  }
}

/**
 * Handle the Enter key to send the message.
 *
 * @param {KeyboardEvent} event
 */
function handleEnter(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
}