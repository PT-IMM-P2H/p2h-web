"""
Telegram Bot Service untuk menangani command /start dan linking user
Bot ini berjalan sebagai background process terpisah dari FastAPI
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models.user import User

logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Handle /start command from Telegram
    Format: /start <phone_number>
    
    User harus mengirim phone_number mereka untuk link akun
    """
    chat_id = str(message.chat.id)
    username = message.from_user.username
    
    # Parse phone number dari command
    args = message.text.split()
    
    if len(args) < 2:
        await message.answer(
            "🔗 <b>Link Akun Telegram Anda</b>\n\n"
            "Untuk menerima notifikasi P2H, kirim command:\n"
            "<code>/start NOMOR_TELEPON_ANDA</code>\n\n"
            "Contoh:\n"
            "<code>/start 081234567890</code>\n\n"
            "⚠️ Gunakan nomor telepon yang sama dengan akun P2H Anda.",
            parse_mode="HTML"
        )
        return
    
    phone_number = args[1].strip()
    
    # Normalisasi phone number (hapus spasi, dash, dll)
    phone_number = phone_number.replace(" ", "").replace("-", "").replace("+", "")
    
    # Cari user berdasarkan phone_number
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        
        if not user:
            await message.answer(
                "❌ <b>Nomor tidak ditemukan</b>\n\n"
                f"Nomor <code>{phone_number}</code> tidak terdaftar di sistem P2H.\n\n"
                "Pastikan:\n"
                "• Nomor sudah terdaftar di sistem\n"
                "• Format nomor benar (contoh: 081234567890)\n"
                "• Tidak ada spasi atau karakter khusus",
                parse_mode="HTML"
            )
            logger.warning(f"Phone number not found: {phone_number}")
            return
        
        # Update telegram_chat_id
        from datetime import datetime
        user.telegram_chat_id = chat_id
        user.telegram_username = username
        user.telegram_linked_at = datetime.utcnow()
        db.commit()
        
        await message.answer(
            f"✅ <b>Berhasil Terhubung!</b>\n\n"
            f"Akun Telegram Anda telah terhubung dengan:\n"
            f"• Nama: <b>{user.full_name}</b>\n"
            f"• Nomor: <code>{user.phone_number}</code>\n"
            f"• Role: <b>{user.role.value}</b>\n\n"
            f"🔔 Anda akan menerima notifikasi P2H di chat ini.\n\n"
            f"Terima kasih! 🙏",
            parse_mode="HTML"
        )
        
        logger.info(f"✅ User {user.phone_number} linked with chat_id {chat_id}")
        
    except Exception as e:
        logger.error(f"Error linking user: {str(e)}", exc_info=True)
        await message.answer(
            "❌ <b>Terjadi kesalahan</b>\n\n"
            "Mohon coba lagi atau hubungi administrator.",
            parse_mode="HTML"
        )
    finally:
        db.close()


@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    """Check current telegram link status"""
    chat_id = str(message.chat.id)
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_chat_id == chat_id).first()
        
        if not user:
            await message.answer(
                "❌ <b>Belum Terhubung</b>\n\n"
                "Telegram Anda belum terhubung dengan akun P2H.\n\n"
                "Gunakan command:\n"
                "<code>/start NOMOR_TELEPON_ANDA</code>",
                parse_mode="HTML"
            )
            return
        
        await message.answer(
            f"✅ <b>Status: Terhubung</b>\n\n"
            f"• Nama: <b>{user.full_name}</b>\n"
            f"• Nomor: <code>{user.phone_number}</code>\n"
            f"• Role: <b>{user.role.value}</b>\n"
            f"• Email: {user.email or '-'}\n"
            f"• Terhubung sejak: {user.telegram_linked_at.strftime('%d/%m/%Y %H:%M') if user.telegram_linked_at else '-'}\n\n"
            f"🔔 Notifikasi P2H aktif.",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"Error checking status: {str(e)}", exc_info=True)
        await message.answer("❌ Terjadi kesalahan saat mengecek status.")
    finally:
        db.close()


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Show help message"""
    await message.answer(
        "📖 <b>Bantuan Bot P2H</b>\n\n"
        "<b>Command yang tersedia:</b>\n\n"
        "• <code>/start NOMOR_HP</code>\n"
        "  Hubungkan akun Telegram dengan akun P2H\n"
        "  Contoh: /start 081234567890\n\n"
        "• <code>/status</code>\n"
        "  Cek status koneksi akun Anda\n\n"
        "• <code>/help</code>\n"
        "  Tampilkan pesan bantuan ini\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 <b>Catatan:</b>\n"
        "• Gunakan nomor HP yang sama dengan akun P2H Anda\n"
        "• Setelah terhubung, Anda akan menerima notifikasi otomatis\n"
        "• Untuk pertanyaan, hubungi administrator sistem",
        parse_mode="HTML"
    )


async def start_bot():
    """Start the telegram bot"""
    try:
        logger.info("🤖 Starting Telegram Bot...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Bot error: {str(e)}", exc_info=True)
    finally:
        await bot.session.close()


def run_bot():
    """Run bot in asyncio event loop"""
    asyncio.run(start_bot())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    run_bot()
