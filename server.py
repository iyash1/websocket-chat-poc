import asyncio
import websockets
import json
import asyncpg
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style

# ----------------- ENVIRONMENT ---------------- #
load_dotenv()
init(autoreset=True)

connected_users = {}
connected_sockets = {}
db_pool = None

# ---------------- DATABASE ---------------- #
# Initialize the database connection pool
async def init_db():
    try: 
        global db_pool
        db_pool = await asyncpg.create_pool(
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            database=os.getenv("PG_DATABASE"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT")
        )
        print(f"{Fore.GREEN} 📀 Database connection pool initialized.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED} ❌ Failed to initialize database connection pool: {e}{Style.RESET_ALL}")
        raise

# Create tables if they don't exist
async def save_user(username):
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO ws_users (username)
            VALUES ($1)
            ON CONFLICT (username) DO NOTHING
        """, username)

# Save messages to the database
async def save_message(sender, recipient, message, message_type):
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO ws_messages (sender, recipient, message, message_type)
            VALUES ($1, $2, $3, $4)
        """, sender, recipient, message, message_type)

# Load recent messages for new connections
async def load_recent_messages(limit=20):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT sender, recipient, message, message_type, created_at
            FROM ws_messages
            ORDER BY created_at DESC
            LIMIT $1
        """, limit)

        return list(reversed(rows))


# ---------------- WEBSOCKET ---------------- #
# Handle incoming WebSocket connections and messages
async def handler(websocket):
    try:
        # Expect the first message to be a registration with a username
        registration_raw = await websocket.recv()
        registration = json.loads(registration_raw)

        # Validate registration message format and type before proceeding
        if registration.get("type") != "register":
            await websocket.close()
            return

        # Extract and validate the username
        username = registration.get("username", "").strip()

        # Check if the username is valid and not already taken
        if not username or username in connected_users:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Invalid or duplicate username."
            }))
            await websocket.close()
            print(f"{Fore.RED} ⚠️ Connection attempt with invalid or duplicate username: '{username}'{Style.RESET_ALL}")
            return

        # Register the user and store the WebSocket connection
        connected_users[username] = websocket
        connected_sockets[websocket] = username

        # Save the user to the database (if not already present)
        await save_user(username)

        print(f"{Fore.GREEN} 👤 {username} connected.✅{Style.RESET_ALL}")

        # Load chat history
        recent_messages = await load_recent_messages()

        for row in recent_messages:
            await websocket.send(json.dumps({
                "type": row["message_type"],
                "from": row["sender"],
                "to": row["recipient"],
                "message": row["message"]
            }))

        # Notify all users about the new connection
        await broadcast_system(f"{username} joined the chat")

        # Handle incoming messages from the client
        async for message_raw in websocket:
            # Validate message format before processing
            data = json.loads(message_raw)
            sender = connected_sockets.get(websocket)

            # Ensure the sender is valid and the message is not empty
            if not sender:
                continue

            # Validate message content and type before processing 
            msg = data.get("message", "").strip()
            if not msg:
                continue

            # Handle broadcast and private messages based on the message type
            if data.get("type") == "broadcast":
                await save_message(sender, None, msg, "broadcast")
                await broadcast_message(sender, msg)

            elif data.get("type") == "private":
                recipient = data.get("to", "").strip()

                # Validate recipient before processing the private message 
                if recipient in connected_users:
                    await save_message(sender, recipient, msg, "private")
                    await private_message(sender, recipient, msg)
                else:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Recipient not found."
                    }))
                    print(f"{Fore.RED} ⚠️ Private message attempt to invalid recipient: '{recipient}'{Style.RESET_ALL}")

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        # Clean up on disconnect
        username = connected_sockets.get(websocket)

        # Only attempt to clean up if the username is valid and exists in the connected users
        if username:
            del connected_users[username]
            del connected_sockets[websocket]
            await broadcast_system(f"{username} left the chat")
            print(f"{Fore.YELLOW} 👤 {username} disconnected.✅{Style.RESET_ALL}")

# Broadcast a message to all connected users 
async def broadcast_message(sender, message):
    payload = json.dumps({
        "type": "broadcast",
        "from": sender,
        "message": message
    })

    for ws in connected_users.values():
        await ws.send(payload)

# Send a private message to a specific recipient 
async def private_message(sender, recipient, message):
    payload = json.dumps({
        "type": "private",
        "from": sender,
        "message": message
    })

    await connected_users[recipient].send(payload)

# Broadcast a system message to all users (e.g., user joined/left notifications)
async def broadcast_system(message):
    payload = json.dumps({
        "type": "system",
        "message": message
    })

    for ws in connected_users.values():
        await ws.send(payload)

# Start the WebSocket server and initialize the database connection pool
async def main():
    await init_db()

    async with websockets.serve(handler, "localhost", 8765):
        print(f"{Fore.GREEN}\n 🌏 Chat server running on ws://localhost:8765 \n{Style.RESET_ALL}")
        await asyncio.Future()

# Run the main function to start the server
if __name__ == "__main__":
    asyncio.run(main())