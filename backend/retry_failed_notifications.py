"""
Retry sending failed telegram notifications
"""
import asyncio
from app.database import SessionLocal
from app.models.notification import TelegramNotification
from app.services.telegram_service import telegram_service
from datetime import datetime

async def retry_failed_notifications():
    db = SessionLocal()
    
    # Get all failed notifications
    failed = db.query(TelegramNotification).filter(
        TelegramNotification.is_sent == False
    ).all()
    
    print(f"\n📤 Retrying {len(failed)} failed notifications...")
    print("=" * 80)
    
    success_count = 0
    for notif in failed:
        print(f"\n🔄 Retrying notification {notif.id}")
        print(f"   Type: {notif.notification_type}")
        print(f"   Vehicle: {notif.vehicle.no_lambung if notif.vehicle else 'N/A'}")
        
        # Try to send
        success = await telegram_service.send_message(notif.message)
        
        if success:
            notif.is_sent = True
            notif.sent_at = datetime.utcnow()
            notif.error_message = None
            print(f"   ✅ SUCCESS - Message sent!")
            success_count += 1
        else:
            print(f"   ❌ FAILED - Still cannot send")
        
        db.commit()
    
    print("\n" + "=" * 80)
    print(f"✅ Successfully sent: {success_count}/{len(failed)}")
    print(f"❌ Still failed: {len(failed) - success_count}/{len(failed)}")
    print("=" * 80)
    
    db.close()

if __name__ == "__main__":
    asyncio.run(retry_failed_notifications())
