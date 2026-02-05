"""
Router untuk menangani Telegram Bot Webhook.
Menerima update dari Telegram Bot API ketika user melakukan /start atau mengirim pesan.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.telegram_service import telegram_service
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/telegram", tags=["telegram"])


@router.post("/webhook")
async def telegram_webhook(
    update: dict,
    db: Session = Depends(get_db)
):
    """
    Webhook endpoint untuk menerima update dari Telegram Bot.
    
    Digunakan untuk:
    1. Mendeteksi ketika user melakukan /start pada bot
    2. Menyimpan chat_id user ke database
    3. Memungkinkan sistem mengirim notifikasi ke user tersebut
    
    Setup di Telegram:
    ```
    POST https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-domain.com/api/telegram/webhook
    ```
    """
    
    try:
        # Tangkap message dari Telegram
        if "message" in update:
            message = update["message"]
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")
            from_user = message.get("from", {})
            
            logger.info(f"📨 Received Telegram message from {chat_id}: {text}")
            
            # Handle /start command
            if text == "/start" and chat_id:
                user = await telegram_service.register_user(
                    db=db,
                    chat_id=str(chat_id),
                    first_name=from_user.get("first_name"),
                    last_name=from_user.get("last_name"),
                    username=from_user.get("username")
                )
                
                # Send welcome message
                welcome_message = f"""
✅ <b>Halo {from_user.get('first_name', 'User')}!</b>

Anda telah berhasil subscribe ke notifikasi P2H System PT. IMM.

📱 Dari sekarang Anda akan menerima notifikasi otomatis untuk:

✅ <b>P2H Status ABNORMAL</b> (Unit tidak boleh operasi)
✅ <b>P2H Status WARNING</b> (Unit perlu perbaikan)  
📅 <b>STNK/KIR akan expired</b> (7 hari sebelumnya)
🚫 <b>STNK/KIR sudah expired</b> (notifikasi urgent)

━━━━━━━━━━━━━━━━━━━━
💡 Jangan tutup atau block bot ini untuk tetap menerima notifikasi.

Terima kasih telah menggunakan sistem P2H Digital PT. IMM 🙏
                """.strip()
                
                await telegram_service.send_message_to_chat_id(
                    str(chat_id), 
                    welcome_message
                )
                
                logger.info(f"✅ Welcome message sent to {user.chat_id}")
                
                return {"status": "ok", "action": "user_registered"}
            
            # Log other messages
            logger.info(f"📝 Message from {chat_id}: {text}")
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"❌ Error processing webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/count")
async def get_registered_users_count(db: Session = Depends(get_db)):
    """Get total count of registered Telegram users"""
    count = await telegram_service.get_registered_users_count(db)
    return {
        "status": "ok",
        "registered_users": count,
        "message": f"Total {count} user(s) terdaftar dan siap menerima notifikasi"
    }


@router.get("/users/list")
async def list_registered_users(db: Session = Depends(get_db)):
    """List semua registered Telegram users (admin only)"""
    from app.models.notification import TelegramUser
    
    users = db.query(TelegramUser).filter(
        TelegramUser.is_active == True
    ).order_by(TelegramUser.started_at.desc()).all()
    
    user_list = [
        {
            "chat_id": user.chat_id,
            "name": f"{user.first_name or ''} {user.last_name or ''}".strip(),
            "username": user.username,
            "started_at": user.started_at.isoformat(),
            "last_notification_at": user.last_notification_at.isoformat() if user.last_notification_at else None
        }
        for user in users
    ]
    
    return {
        "status": "ok",
        "total_users": len(user_list),
        "users": user_list
    }


@router.post("/test-message")
async def send_test_message(db: Session = Depends(get_db)):
    """Send test notification to all registered users"""
    message = """
🧪 <b>TEST NOTIFIKASI</b>
━━━━━━━━━━━━━━━━━━━━
✅ Sistem Telegram sudah terkonfigurasi dengan benar!

Bot ini siap mengirimkan notifikasi real-time untuk:
• ❌ P2H Status ABNORMAL
• ⚠️ P2H Status WARNING
• 📅 STNK/KIR akan expired
• 🚫 STNK/KIR sudah expired

━━━━━━━━━━━━━━━━━━━━
<i>Notifikasi Sistem P2H PT IMM</i>
    """.strip()
    
    success = await telegram_service._send_to_all_users(db, message)
    
    registered_count = await telegram_service.get_registered_users_count(db)
    
    return {
        "status": "ok" if success else "failed",
        "message": "Test message sent successfully" if success else "Failed to send test message",
        "registered_users": registered_count
    }
