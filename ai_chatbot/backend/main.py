"""
FastAPI backend for a simple AI chatbot.

This application exposes a single POST endpoint at `/chat`. When a message is
sent, it forwards the message to OpenAI’s API and returns the assistant’s
reply. The API key must be provided via the `OPENAI_API_KEY` environment
variable.
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read the API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable is not set.")
openai.api_key = OPENAI_API_KEY


class ChatRequest(BaseModel):
    """Schema for incoming chat requests."""

    message: str


class ChatResponse(BaseModel):
    """Schema for outgoing chat responses."""

    reply: str


app = FastAPI(
    title="AI Chatbot API",
    description=(
        "A simple API that forwards user messages to OpenAI's GPT models "
        "and returns the assistant's reply."
    ),
)


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest) -> ChatResponse:
    """
    POST endpoint for chatting with the AI.

    Parameters
    ----------
    chat_request : ChatRequest
        The incoming request containing the user's message.

    Returns
    -------
    ChatResponse
        The assistant's reply.
    """
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY environment variable is not set on the server.",
        )

    user_message = chat_request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        # Call OpenAI's API to get a response
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use GPT-4o to reduce cost and improve latency
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful, concise assistant in a web chat. "
                        "Answer as clearly and directly as possible."
                    ),
                },
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
        )
        reply_text = response.choices[0].message["content"].strip()
        return ChatResponse(reply=reply_text)
    except Exception as exc:
        logger.exception("Error communicating with OpenAI API: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while communicating with the language model.",
        ) from exc