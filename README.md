# AI Chatbot for Private Website

This project provides a simple chat application where users can interact with an AI assistant. It consists of a Python FastAPI backend that communicates with OpenAI’s API and a static front‑end written in HTML and JavaScript. You can host the backend and front‑end on your own infrastructure (e.g. Render, Vercel, or a VPS) to build a privately hosted AI chatbot.

## Directory structure

```
ai_chatbot/
├── backend/
│   ├── main.py
│   ├── requirements.txt
├── frontend/
│   ├── index.html
│   └── script.js
```

- **backend/** – Contains the FastAPI application and dependencies.
- **frontend/** – A simple chat UI that sends requests to the backend.
- **README.md** – This document with setup and deployment instructions.

## Prerequisites

- Python 3.8 or later.
- An OpenAI API key with access to GPT‑4o-mini or GPT‑4.
- A hosting provider (Render, Vercel, or your own VPS) for both the backend and front‑end.

## Backend setup

1. **Install dependencies:**

   Navigate into the `backend/` directory and install the required packages.

   ```bash
   cd ai_chatbot/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure the API key:**

   The FastAPI application expects an environment variable called `OPENAI_API_KEY` containing your OpenAI API key. You can set it in your shell before starting the server:

   ```bash
   export OPENAI_API_KEY=sk-...
   ```

   On Windows PowerShell:

   ```powershell
   $env:OPENAI_API_KEY = "sk-..."
   ```

3. **Run the development server locally:**

   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The backend will start at `http://localhost:8000`. The `/chat` endpoint accepts POST requests with a JSON body of the form:

   ```json
   { "message": "Your question here" }
   ```

   and returns a JSON response:

   ```json
   { "reply": "AI response here" }
   ```

## Front‑end setup

The front‑end is a static site. You can open `frontend/index.html` in a browser for local testing. By default, it expects the backend to be running on `http://localhost:8000`. You can change the API URL in `frontend/script.js` by editing the `API_URL` constant.

### Run locally

Open another terminal window and run a simple HTTP server to serve the front‑end files. For example:

```bash
cd ai_chatbot/frontend
python -m http.server 9000
```

Then visit `http://localhost:9000` in your browser. Enter a message in the text box and click **Send**; the chat UI will send your message to the backend and display the response.

## Deploying your chatbot

There are many ways to deploy this application. Below are high‑level steps for common platforms. You’ll need separate deployments for the backend (FastAPI) and the front‑end (static assets).

### Deploy backend on Render

1. **Create a new Web Service** in your Render dashboard.
2. Choose **Docker** or **Python** service. For a Python service, set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
   - **Environment Variables:** Set `OPENAI_API_KEY`.
3. Ensure that Render exposes port `10000` or whichever port you specify in the start command.

### Deploy backend on Vercel

Vercel is optimized for Node.js and static sites; it can run Python via functions but isn’t ideal for persistent FastAPI servers. For reliable FastAPI hosting, use Render or a VPS instead.

### Deploy backend on a VPS (e.g. DigitalOcean, AWS Lightsail)

1. SSH into your server and install Python 3.
2. Clone or upload the `ai_chatbot/backend` directory.
3. Install dependencies (`pip install -r requirements.txt`) and set your `OPENAI_API_KEY`.
4. Use a process manager like **gunicorn** or **uvicorn** behind a reverse proxy (nginx or Apache) to serve the app.

Example systemd service for running uvicorn:

```ini
[Unit]
Description=AI Chatbot FastAPI Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/ai_chatbot/backend
Environment="OPENAI_API_KEY=sk-..."
ExecStart=/usr/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Deploy front‑end on Render or Vercel

The front‑end is a static site. Both platforms support static hosting:

- **Render:** create a **Static Site** and point it to `ai_chatbot/frontend`. Set the build command to `""` (empty) and the static root to `/`.
- **Vercel:** run `vercel` in the `frontend` folder; it will detect that the site is static and deploy it.

Update the `API_URL` in `script.js` to point to your deployed backend (for example: `https://your-backend.onrender.com/chat`).

### Deploy front‑end on a VPS

You can also host the static files on your VPS. Configure your web server to serve the contents of `ai_chatbot/frontend`. For example, with nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/ai_chatbot/frontend;
        index index.html;
        try_files $uri $uri/ =404;
    }
}
```

Be sure to update `API_URL` in `script.js` to the public URL of your backend.

## Customizing the chatbot

- You can modify the system prompt or the model used by editing `backend/main.py` in the `create_chat_completion` function call.
- To add memory or more advanced features, maintain a conversation history on the server or integrate with a database.
- For a more complex front‑end, consider rewriting the UI in React or another framework.

---

Enjoy building your private AI chatbot! Feel free to adapt this project to suit your needs.
