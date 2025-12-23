from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from db.database import get_db
from models.messages import Conversation, Message
from models.userModels import User
import firebase_admin
from firebase_admin import credentials, messaging
import random
import string

router = APIRouter()

# ================= FIREBASE INIT ================= #

if not firebase_admin._apps:
    cred = credentials.Certificate(
        "./utils/mmp--mymarketplace-firebase-adminsdk-fbsvc-035dfb94f3.json"
    )
    firebase_admin.initialize_app(cred)

# ================= HELPERS ================= #

def generate_random_string(length=10):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def send_notification(token: str, title: str, body: str, user_id: int, fullname: str):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            data={
                "userid": str(user_id),
                "fullname": fullname or ""
            }
        )
        response = messaging.send(message)
        print("✅ Notification sent:", response)
        return response

    except messaging.UnregisteredError:
        print(f"⚠️ Invalid FCM token for user {user_id}")
        return None

    except Exception as e:
        print("❌ FCM error:", e)
        return None


# ================= CONNECTION MANAGER ================= #

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def send_private_message(
        self,
        sender_id: int,
        receiver_id: int,
        message: str,
        db: Session
    ):
        msg = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)

        conversation = db.query(Conversation).filter(
            ((Conversation.user1_id == sender_id) & (Conversation.user2_id == receiver_id)) |
            ((Conversation.user1_id == receiver_id) & (Conversation.user2_id == sender_id))
        ).first()

        if not conversation:
            conversation = Conversation(
                user1_id=sender_id,
                user2_id=receiver_id,
                last_message_id=msg.id
            )
            db.add(conversation)
        else:
            conversation.last_message_id = msg.id

        db.commit()

        receiver_socket = self.active_connections.get(receiver_id)
        if receiver_socket:
            await receiver_socket.send_json({
                "id": msg.id,
                "sender_id": sender_id,
                "message": message
            })


manager = ConnectionManager()

# ================= WEBSOCKET ================= #

@router.websocket("/chat/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    db: Session = next(get_db())

    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()

            receiver_id = data.get("receiver_id")
            message = data.get("message")

            if not receiver_id or not message:
                await websocket.send_json({
                    "error": "receiver_id and message required"
                })
                continue

            receiver_id = int(receiver_id)

            sender = db.query(User).filter(User.id == user_id).first()
            receiver = db.query(User).filter(User.id == receiver_id).first()

            if not receiver:
                await websocket.send_json({"error": "Receiver not found"})
                continue

            # 🔔 Push Notification
            if receiver.fcm_token:
                send_notification(
                    token=receiver.fcm_token,
                    title=sender.full_name if sender else "New Message",
                    body=message,
                    user_id=user_id,
                    fullname=sender.full_name if sender else ""
                )

            # 💾 Save + Send Message
            await manager.send_private_message(
                sender_id=user_id,
                receiver_id=receiver_id,
                message=message,
                db=db
            )

            # 🟢 Update last active
            if sender:
                sender.last_active_at = func.now()
                db.commit()

    except WebSocketDisconnect:
        manager.disconnect(user_id)
