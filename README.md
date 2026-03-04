# 🗨️ WebSocket Chat POC

This project demonstrates a simple real-time chat application using Python, WebSockets, and HTML/JS.  
You can broadcast messages to all users or send private messages to specific users. 🚀

---

## 📦 Project Structure

```
websocket-chat-poc/
├── server.py           # Python WebSocket server
├── index.html          # Simple chat client (HTML/JS)
├── requirements.txt    # Python dependencies
└── README.md           # This documentation
```

---

## 🛠️ Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (recommended for environment management)
- Python 3.8+
- A modern web browser

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd websocket-chat-poc
```

### 2. Create & Activate Conda Environment

```bash
conda create -n ws-chat-poc python=3.10
conda activate ws-chat-poc
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application

### 1. Start the WebSocket Server

```bash
python server.py
```

You should see:  
`Server running at ws://localhost:8765`

### 2. Open the Chat Client

Just open `index.html` in your browser (double-click or use `file://` path).

> **Note:** The client connects to `ws://localhost:8765` by default.

---

## 💡 How It Works

- **Register:** Enter a username and click "Join".
- **Send Message:**  
    - Leave "Recipient" empty to broadcast to all users.  
    - Enter a username in "Recipient" for a private message.
- **Messages:**  
    - `[Broadcast]` - Sent to everyone  
    - `[Private]` - Sent only to the specified user  
    - `[System]` - Join/leave notifications

---

## 📝 Requirements

- `websockets`  
- `asyncio`  
- `json` (Python built-in)

All dependencies are listed in `requirements.txt`.

---

## ❓ FAQ

**Q:** Can I run multiple clients?  
**A:** Yes! Open `index.html` in multiple browser tabs/windows.

**Q:** Can I deploy this?  
**A:** This is a POC for local/demo use. For production, consider authentication, HTTPS, and security improvements.

---

## 🤝 Contributing

Feel free to fork, improve, and submit PRs!  
Suggestions and feedback are welcome.

---

## 📧 Contact

For questions, reach out via GitHub Issues.

---

Happy chatting! 🎉