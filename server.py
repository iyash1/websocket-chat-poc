import asyncio
import websockets
import json

connected_users = {}       # username -> websocket
connected_sockets = {}     # websocket -> username


async def handler(websocket):
    try:
        # Expect registration first
        registration_raw = await websocket.recv()
        registration = json.loads(registration_raw)

        if registration.get("type") != "register":
            await websocket.close()
            return

        username = registration.get("username", "").strip()

        # Validate username
        if not username:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Username cannot be empty."
            }))
            await websocket.close()
            return

        if username in connected_users:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Username already taken."
            }))
            await websocket.close()
            return

        # Store mappings
        connected_users[username] = websocket
        connected_sockets[websocket] = username

        print(f"{username} connected")
        await broadcast_system(f"{username} joined the chat")

        # Listen for messages
        async for message_raw in websocket:
            data = json.loads(message_raw)

            sender = connected_sockets.get(websocket)

            if not sender:
                continue

            msg = data.get("message", "").strip()

            if not msg:
                continue  # Ignore empty messages

            if data.get("type") == "broadcast":
                await broadcast_message(sender, msg)

            elif data.get("type") == "private":
                recipient = data.get("to", "").strip()

                if recipient and recipient in connected_users:
                    await private_message(sender, recipient, msg)
                else:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Recipient not found."
                    }))

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        # Cleanup on disconnect
        username = connected_sockets.get(websocket)

        if username:
            del connected_users[username]
            del connected_sockets[websocket]
            print(f"{username} disconnected")
            await broadcast_system(f"{username} left the chat")


async def broadcast_message(sender, message):
    payload = json.dumps({
        "type": "broadcast",
        "from": sender,
        "message": message
    })

    for ws in connected_users.values():
        await ws.send(payload)


async def private_message(sender, recipient, message):
    payload = json.dumps({
        "type": "private",
        "from": sender,
        "message": message
    })

    await connected_users[recipient].send(payload)


async def broadcast_system(message):
    payload = json.dumps({
        "type": "system",
        "message": message
    })

    for ws in connected_users.values():
        await ws.send(payload)


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server running at ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())