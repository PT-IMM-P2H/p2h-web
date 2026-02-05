"""
Script untuk setup Telegram Multi-User Bot
- Setup webhook
- Menambahkan subscriber awal
- Test broadcast
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import httpx
from sqlalchemy import create_engine, text
from datetime import datetime
from app.config import settings

# Bot configuration
BOT_TOKEN = "8169592330:AAFgIDyHTfPi8nDorOuFZytKQPJ30uxQYF0"
INITIAL_CHAT_IDS = ["5625212555", "1778221644", "377036145"]
WEBHOOK_URL = "https://p2h-web-production.up.railway.app/api/telegram/webhook"

async def setup_webhook():
    """Setup webhook untuk bot telegram"""
    print("\n🔧 Setting up Telegram webhook...")
    
    async with httpx.AsyncClient() as client:
        try:
            # Set webhook
            response = await client.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
                json={"url": WEBHOOK_URL}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print(f"✅ Webhook berhasil di-setup: {WEBHOOK_URL}")
                else:
                    print(f"❌ Error setup webhook: {result}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

async def get_bot_info():
    """Dapatkan informasi bot"""
    print("\n📋 Getting bot info...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    bot_info = result.get("result", {})
                    print(f"✅ Bot Name: @{bot_info.get('username')}")
                    print(f"✅ Bot ID: {bot_info.get('id')}")
                    print(f"✅ Bot First Name: {bot_info.get('first_name')}")
                else:
                    print(f"❌ Error: {result}")
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def add_initial_subscribers():
    """Menambahkan subscriber awal ke database"""
    print("\n👥 Adding initial subscribers...")
    
    try:
        engine = create_engine(settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://"))
        
        with engine.connect() as conn:
            # Check if table exists
            result = conn.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'telegram_subscribers')"
            ))
            table_exists = result.scalar()
            
            if not table_exists:
                print("❌ Table telegram_subscribers tidak ada. Jalankan migrasi dulu!")
                return
            
            for chat_id in INITIAL_CHAT_IDS:
                # Check if already exists
                result = conn.execute(text(
                    "SELECT COUNT(*) FROM telegram_subscribers WHERE chat_id = :chat_id"
                ), {"chat_id": chat_id})
                
                if result.scalar() == 0:
                    # Insert new subscriber
                    conn.execute(text("""
                        INSERT INTO telegram_subscribers 
                        (chat_id, chat_type, is_active, notes, subscribed_at) 
                        VALUES (:chat_id, 'private', true, 'Initial admin subscriber', :now)
                    """), {"chat_id": chat_id, "now": datetime.utcnow()})
                    print(f"✅ Added subscriber: {chat_id}")
                else:
                    print(f"ℹ️  Subscriber {chat_id} sudah ada")
            
            conn.commit()
            print("✅ Semua subscriber awal berhasil ditambahkan")
            
    except Exception as e:
        print(f"❌ Error menambahkan subscriber: {str(e)}")

async def send_test_message():
    """Kirim pesan test ke semua subscriber"""
    print("\n🧪 Sending test message...")
    
    test_message = """
🎉 <b>TELEGRAM MULTI-USER SETUP BERHASIL!</b>

Sistem notifikasi P2H PT. IMM sekarang mendukung multi-user!

<b>✅ Fitur yang tersedia:</b>
• Notifikasi P2H Abnormal/Warning otomatis
• Alert dokumen STNK/KIR expired
• Broadcast message dari admin

<b>📱 Commands:</b>
/start - Subscribe notifikasi
/stop - Unsubscribe 
/status - Cek status
/help - Bantuan

<i>🔔 Bot: @imm_p2h_bot</i>
<i>🏢 PT. IMM Bontang</i>
    """
    
    async with httpx.AsyncClient() as client:
        for chat_id in INITIAL_CHAT_IDS:
            try:
                response = await client.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": test_message.strip(),
                        "parse_mode": "HTML"
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        print(f"✅ Test message berhasil dikirim ke {chat_id}")
                    else:
                        print(f"❌ Gagal kirim ke {chat_id}: {result}")
                else:
                    print(f"❌ HTTP Error untuk {chat_id}: {response.status_code}")
                    
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Exception untuk {chat_id}: {str(e)}")

async def main():
    """Main function untuk setup lengkap"""
    print("=" * 60)
    print("🤖 TELEGRAM MULTI-USER SETUP - PT. IMM P2H BOT")
    print("=" * 60)
    print(f"Bot Token: {BOT_TOKEN}")
    print(f"Initial Chat IDs: {INITIAL_CHAT_IDS}")
    print(f"Webhook URL: {WEBHOOK_URL}")
    
    # 1. Get bot info
    await get_bot_info()
    
    # 2. Setup webhook
    await setup_webhook()
    
    # 3. Add initial subscribers
    add_initial_subscribers()
    
    # 4. Send test message
    await send_test_message()
    
    print("\n" + "=" * 60)
    print("✅ SETUP SELESAI!")
    print("=" * 60)
    print("\n📋 Langkah selanjutnya:")
    print("1. User lain bisa kirim /start ke @imm_p2h_bot untuk subscribe")
    print("2. Admin bisa gunakan API /api/telegram/broadcast untuk broadcast")
    print("3. Sistem akan otomatis kirim notifikasi P2H ke semua subscriber")
    print("\n🔗 API Documentation: https://p2h-web-production.up.railway.app/docs#/Telegram")

if __name__ == "__main__":
    asyncio.run(main())