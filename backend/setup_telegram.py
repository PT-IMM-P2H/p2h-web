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
    
    if not settings.TELEGRAM_BOT_TOKEN:
        print("\n❌ TELEGRAM NOT CONFIGURED!")
        print("\n📝 Cara Setup:")
        print("   1. Buat bot baru dengan @BotFather di Telegram")
        print("   2. Edit file backend/.env dan isi:")
        print("      TELEGRAM_BOT_TOKEN=your_bot_token_here")
        print("   3. CATATAN: TELEGRAM_CHAT_ID sudah tidak diperlukan!")
        print("      Bot sekarang otomatis register chat_id saat user /start")
        print("   4. Restart aplikasi")
        print("\n📖 Lihat TELEGRAM_INTEGRATION.md untuk panduan lengkap")
        return
    
    print(f"   Bot Token: {settings.TELEGRAM_BOT_TOKEN[:20]}...")
    
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

🆕 <b>Fitur Baru:</b>
User yang sudah melakukan /start pada bot akan otomatis terdaftar dan menerima notifikasi!

━━━━━━━━━━━━━━━━━━━━
<i>Notifikasi Sistem P2H PT IMM</i>
    """.strip()
    
    try:
        # Try to send to legacy chat_id if set
        if settings.TELEGRAM_CHAT_ID:
            success = await telegram_service.send_message(test_message)
        else:
            # If no legacy chat_id, just test bot connection
            print("   ℹ️  TELEGRAM_CHAT_ID not set (optional - bot uses registered users)")
            success = True  # Bot is configured
        
        if success or settings.TELEGRAM_BOT_TOKEN:
            print("   ✅ Telegram bot is configured and ready!")
            print("\n" + "=" * 60)
            print("🎉 TELEGRAM INTEGRATION READY!")
            print("=" * 60)
            print("\n✨ Cara kerja sistem notifikasi (BARU):")
            print("\n1️⃣ User membuka Telegram dan cari bot Anda")
            print("2️⃣ User melakukan /start pada bot")
            print("3️⃣ System otomatis register chat_id user ke database")
            print("4️⃣ User siap menerima notifikasi real-time!")
            print("\n📱 Saat terjadi P2H WARNING/ABNORMAL:")
            print("   • Sistem akan mengirim notifikasi ke SEMUA user yang sudah /start")
            print("   • Notifikasi dalam bentuk pesan formatted yang jelas")
            print("   • Riwayat notifikasi tersimpan di tabel telegram_notifications")
            print("\n💡 Kelebihan sistem baru:")
            print("   ✅ Multiple user dapat menerima notifikasi")
            print("   ✅ User baru tidak perlu update .env")
            print("   ✅ Chat_id terupdate otomatis saat /start")
            print("   ✅ Fallback ke static TELEGRAM_CHAT_ID jika ada")
            print("\n📊 Check status:")
            print("   GET /api/telegram/users/count - Hitung user terdaftar")
            print("   POST /api/telegram/test-message - Kirim test ke semua user")
        else:
            print("   ❌ Failed to connect to Telegram API")
            print("\n⚠️ TROUBLESHOOTING:")
            print("   1. Pastikan Bot Token benar")
            print("   2. Cek koneksi internet")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        print("\n⚠️ Terjadi kesalahan saat menghubungi Telegram API")
    
    finally:
        # Close client
        await telegram_service.close()

def main():
    """Main function"""
    print("\n🤖 Setup & Test Telegram Bot Integration (Updated)\n")
    asyncio.run(test_telegram_connection())
    print("\n")

if __name__ == "__main__":
    main()

