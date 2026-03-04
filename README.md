# 🗨️ WebSocket Chat POC

This project demonstrates a simple real-time chat application using Python, WebSockets, PostgreSQL, and HTML/JS.  
You can broadcast messages to all users or send private messages to specific users. 🚀  
All chat history and users are persisted in a PostgreSQL database.

---

## 📦 Project Structure

```
websocket-chat-poc/
├── server.py           # Python WebSocket server (with PostgreSQL integration)
├── index.html          # Simple chat client (HTML/JS)
├── requirements.txt    # Python dependencies
├── .env                # Database connection settings
└── README.md           # This documentation
```

---

## 🛠️ Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (recommended for environment management)
- Python 3.8+
- PostgreSQL server (local or remote)
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

### 4. Configure Database

Edit the `.env` file with your PostgreSQL credentials:

```env
PG_USER="<YOUR_PG_USERNAME>"
PG_PASSWORD="<YOUR_PG_PASSWORD>"
PG_DATABASE="<YOUR_PG_DATABASE_NAME>"
PG_HOST="<YOUR_PG_HOST_IP | localhost>"
PG_PORT="5432"
```

### 5. Create Database Tables

Run the following SQL in your PostgreSQL database:

```sql
CREATE TABLE IF NOT EXISTS ws_users (
    username TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS ws_messages (
    id SERIAL PRIMARY KEY,
    sender TEXT,
    recipient TEXT,
    message TEXT,
    message_type TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 🚀 Running the Application

### 1. Start the WebSocket Server

```bash
python server.py
```

You should see:  
`🌏 Chat server running on ws://localhost:8765`

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
- **Persistence:**  
    - All users and messages are stored in PostgreSQL.
    - New users receive recent chat history on join.

---

## 📝 Requirements

- `websockets`  
- `asyncio`  
- `json`  
- `colorama`  
- `dotenv`  
- `asyncpg`  

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