import asyncio
import websockets
import json

connected_users = {}  # username -> websocket

async def handler(websocket):
    try:
        # First message must be registration
        registration = await websocket.recv()
        data = json.loads(registration)

        if data["type"] != "register":
            await websocket.close()
            return

        username = data["username"]
        connected_users[username] = websocket
        print(f"{username} connected")

        await broadcast_system_message(f"{username} joined the chat")

        async for message in websocket:
            data = json.loads(message)

            if data["type"] == "broadcast":
                await broadcast_message(username, data["message"])

            elif data["type"] == "private":
                await private_message(username, data["to"], data["message"])

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Remove user on disconnect
        for user, ws in list(connected_users.items()):
            if ws == websocket:
                del connected_users[user]
                await broadcast_system_message(f"{user} left the chat")
                break


async def broadcast_message(sender, message):
    payload = json.dumps({
        "type": "broadcast",
        "from": sender,
        "message": message
    })

    for ws in connected_users.values():
        await ws.send(payload)


async def private_message(sender, recipient, message):
    if recipient in connected_users:
        payload = json.dumps({
            "type": "private",
            "from": sender,
            "message": message
        })
        await connected_users[recipient].send(payload)


async def broadcast_system_message(message):
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