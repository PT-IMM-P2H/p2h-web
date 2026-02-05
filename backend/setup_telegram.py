"""
Script untuk setup dan test Telegram Bot
Jalankan: python setup_telegram.py
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings
from app.services.telegram_service import telegram_service

async def test_telegram_connection():
    """Test koneksi ke Telegram Bot"""
    print("=" * 60)
    print("🔍 TESTING TELEGRAM CONFIGURATION")
    print("=" * 60)
    
    # 1. Check environment variables
    print("\n1️⃣ Checking Environment Variables...")
    print(f"   TELEGRAM_BOT_TOKEN: {'✅ Set' if settings.TELEGRAM_BOT_TOKEN else '❌ Empty'}")
    print(f"   TELEGRAM_CHAT_ID: {'✅ Set' if settings.TELEGRAM_CHAT_ID else '❌ Empty'}")
    
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        print("\n❌ TELEGRAM NOT CONFIGURED!")
        print("\n📝 Cara Setup:")
        print("   1. Buat bot baru dengan @BotFather di Telegram")
        print("   2. Dapatkan Chat ID dari @userinfobot")
        print("   3. Edit file backend/.env dan isi:")
        print("      TELEGRAM_BOT_TOKEN=your_bot_token_here")
        print("      TELEGRAM_CHAT_ID=your_chat_id_here")
        print("   4. Restart aplikasi")
        print("\n📖 Lihat TELEGRAM_INTEGRATION.md untuk panduan lengkap")
        return
    
    print(f"   Bot Token: {settings.TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"   Chat ID: {settings.TELEGRAM_CHAT_ID}")
    
    # 2. Test sending message
    print("\n2️⃣ Testing Connection to Telegram API...")
    test_message = """
🧪 <b>TEST NOTIFIKASI P2H SYSTEM</b>
━━━━━━━━━━━━━━━━━━━━
<b>Status:</b> ✅ Koneksi Berhasil!

Bot Telegram sudah terkonfigurasi dengan benar dan siap mengirim notifikasi real-time untuk:

• ❌ P2H Status ABNORMAL
• ⚠️ P2H Status WARNING  
• 📅 STNK/KIR akan expired
• 🚫 STNK/KIR sudah expired

━━━━━━━━━━━━━━━━━━━━
<i>Notifikasi Sistem P2H PT IMM</i>
    """.strip()
    
    try:
        success = await telegram_service.send_message(test_message)
        
        if success:
            print("   ✅ Test message sent successfully!")
            print("\n" + "=" * 60)
            print("🎉 TELEGRAM INTEGRATION READY!")
            print("=" * 60)
            print("\n✨ Sistem notifikasi sudah aktif dan siap digunakan!")
            print("\n📱 Cek Telegram Anda untuk pesan test.")
            print("\n💡 Notifikasi akan otomatis terkirim ketika:")
            print("   • User submit P2H dengan status WARNING/ABNORMAL")
            print("   • Scheduler mendeteksi dokumen akan/sudah expired")
        else:
            print("   ❌ Failed to send test message")
            print("\n⚠️ TROUBLESHOOTING:")
            print("   1. Pastikan Bot Token benar")
            print("   2. Pastikan Chat ID benar")
            print("   3. Pastikan bot sudah di-start (klik /start di chat)")
            print("   4. Cek koneksi internet")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        print("\n⚠️ Terjadi kesalahan saat menghubungi Telegram API")
    
    finally:
        # Close client
        await telegram_service.close()

def main():
    """Main function"""
    print("\n🤖 Setup & Test Telegram Bot Integration\n")
    asyncio.run(test_telegram_connection())
    print("\n")

if __name__ == "__main__":
    main()
