from typing import Optional, List
import logging
import asyncio
from datetime import datetime
import httpx
from sqlalchemy.orm import Session

from app.config import settings
from app.models.notification import TelegramNotification, NotificationType, TelegramUser
from app.models.vehicle import Vehicle
from app.models.p2h import P2HReport, InspectionStatus

logger = logging.getLogger(__name__)

class TelegramService:
    """Service for sending Telegram notifications for P2H and Expiry Alerts"""
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        # Shared client dengan connection pooling untuk performa lebih baik
        self._client = None
    
    def _get_client(self) -> httpx.AsyncClient:
        """Get or create shared async client dengan connection pooling"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0, connect=10.0),  # 30s timeout, 10s connect
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )
        return self._client
    
    async def send_message(self, message: str, max_retries: int = 3) -> bool:
        """Kirim pesan ke Telegram dengan retry mechanism"""
        client = self._get_client()
        
        for attempt in range(max_retries):
            try:
                logger.info(f"📤 Sending telegram message (attempt {attempt + 1}/{max_retries})")
                
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True
                    }
                )
                
                if response.status_code == 200:
                    logger.info(f"✅ Telegram message sent successfully on attempt {attempt + 1}")
                    return True
                elif response.status_code == 400:
                    # Bad request - tidak perlu retry
                    logger.error(f"❌ Telegram API Bad Request: {response.text}")
                    return False
                else:
                    logger.warning(f"⚠️ Telegram API returned {response.status_code}: {response.text}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                        continue
                    return False
                    
            except httpx.TimeoutException as e:
                logger.warning(f"⏱️ Telegram request timeout on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                logger.error(f"❌ All {max_retries} attempts timed out")
                return False
                
            except httpx.NetworkError as e:
                logger.warning(f"🌐 Network error on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                logger.error(f"❌ Network error after {max_retries} attempts")
                return False
                
            except Exception as e:
                logger.error(f"❌ Unexpected error sending telegram: {str(e)}", exc_info=True)
                return False
        
        return False
    
    async def send_message_to_chat_id(self, chat_id: str, message: str, max_retries: int = 3) -> bool:
        """Kirim pesan ke specific chat_id"""
        client = self._get_client()
        
        for attempt in range(max_retries):
            try:
                logger.info(f"📤 Sending message to chat_id {chat_id} (attempt {attempt + 1}/{max_retries})")
                
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": message,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True
                    }
                )
                
                if response.status_code == 200:
                    logger.info(f"✅ Message sent successfully to {chat_id}")
                    return True
                elif response.status_code == 400:
                    logger.error(f"❌ Bad Request to {chat_id}: {response.text}")
                    return False
                else:
                    logger.warning(f"⚠️ API returned {response.status_code} for {chat_id}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    return False
                    
            except Exception as e:
                logger.error(f"❌ Error sending to {chat_id}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return False
        
        return False
    
    def format_p2h_notification(
        self,
        vehicle: Vehicle,
        report: P2HReport,
        status: InspectionStatus
    ) -> str:
        """Format pesan untuk laporan P2H yang bermasalah (Abnormal/Warning)"""
        status_emoji = "❌" if status == InspectionStatus.ABNORMAL else "⚠️"
        status_text = "ABNORMAL (STOP OPERASI)" if status == InspectionStatus.ABNORMAL else "WARNING (PERLU PERBAIKAN)"
        
        # Build detail items yang bermasalah
        problem_items = []
        for detail in report.details:
            if detail.status in [InspectionStatus.ABNORMAL, InspectionStatus.WARNING]:
                # Get checklist item name
                item_name = detail.checklist_item.item_name if detail.checklist_item else "Item tidak diketahui"
                item_status = "❌ ABNORMAL" if detail.status == InspectionStatus.ABNORMAL else "⚠️ WARNING"
                keterangan = detail.keterangan or "Tidak ada keterangan"
                
                problem_items.append(f"• <b>{item_name}</b>\n  Status: {item_status}\n  Keterangan: {keterangan}")
        
        # Format list of problem items
        items_text = "\n\n".join(problem_items) if problem_items else "Tidak ada detail item"
        
        message = f"""
{status_emoji} <b>P2H ALERT: {status_text}</b>
━━━━━━━━━━━━━━━━━━━━
<b>Unit:</b> <code>{vehicle.no_lambung}</code>
<b>Tipe:</b> {vehicle.vehicle_type.value}
<b>Merk/Plat:</b> {vehicle.merk or '-'} / {vehicle.plat_nomor or '-'}

<b>📅 Detail Pemeriksaan:</b>
<b>Tanggal:</b> {report.submission_date.strftime('%d %b %Y')}
<b>Waktu:</b> {report.submission_time.strftime('%H:%M')} WITA
<b>Shift:</b> {report.shift_number}
<b>User:</b> {report.user.full_name if report.user else 'System'}

<b>📝 Status Akhir:</b> {status.value.upper()}

<b>🔍 Item Yang Bermasalah:</b>
{items_text}

<b>⚠️ Tindakan:</b> 
Harap segera melakukan pengecekan unit di workshop terdekat.
━━━━━━━━━━━━━━━━━━━━
<i>Notifikasi Sistem P2H PT IMM</i>
        """
        return message.strip()
    
    def format_expiry_notification(
        self,
        vehicle: Vehicle,
        expiry_type: str,
        expiry_date: datetime,
        days_remaining: int
    ) -> str:
        """Format pesan untuk peringatan STNK/KIR yang akan habis"""
        if days_remaining <= 0:
            urgency = "🚨 <b>SUDAH EXPIRED (STOP OPERASI)</b>"
            emoji = "🚫"
        elif days_remaining <= 7:
            urgency = "🔴 <b>SANGAT SEGERA</b>"
            emoji = "🚨"
        else:
            urgency = "🟡 <b>PERINGATAN</b>"
            emoji = "⚠️"

        message = f"""
{emoji} <b>EXPIRY ALERT: {expiry_type}</b>
━━━━━━━━━━━━━━━━━━━━
<b>Unit:</b> <code>{vehicle.no_lambung}</code>
<b>Plat Nomor:</b> {vehicle.plat_nomor or '-'}

<b>📅 Detail Dokumen:</b>
<b>Jenis:</b> {expiry_type}
<b>Tanggal Expired:</b> {expiry_date.strftime('%d/%m/%Y')}
<b>Sisa Waktu:</b> <b>{days_remaining} Hari Lagi</b>

<b>Status:</b> {urgency}

<b>💡 Info:</b>
Harap segera memproses perpanjangan dokumen agar operasional tidak terganggu.
━━━━━━━━━━━━━━━━━━━━
<i>Notifikasi Sistem P2H PT IMM</i>
        """
        return message.strip()
    
    async def send_p2h_notification(
        self,
        db: Session,
        vehicle: Vehicle,
        report: P2HReport,
        status: InspectionStatus
    ) -> Optional[TelegramNotification]:
        """Kirim notifikasi P2H ke semua registered users dan catat di tabel telegram_notifications"""
        
        if status == InspectionStatus.NORMAL:
            return None
            
        notification_type = (
            NotificationType.P2H_ABNORMAL 
            if status == InspectionStatus.ABNORMAL 
            else NotificationType.P2H_WARNING
        )
        
        message = self.format_p2h_notification(vehicle, report, status)
        
        # Simpan log ke DB
        notification = TelegramNotification(
            notification_type=notification_type,
            vehicle_id=vehicle.id,
            report_id=report.id,
            message=message,
            is_sent=False
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        # Kirim ke semua registered users
        success = await self._send_to_all_users(db, message)
        
        # Update status kirim
        notification.is_sent = success
        if success:
            notification.sent_at = datetime.utcnow()
        else:
            notification.error_message = "Gagal terhubung ke Telegram API atau tidak ada user yang terdaftar"
        
        db.commit()
        return notification
    
    async def send_expiry_notification(
        self,
        db: Session,
        vehicle: Vehicle,
        expiry_type: str,
        expiry_date: datetime,
        days_remaining: int
    ) -> Optional[TelegramNotification]:
        """Kirim notifikasi Expired ke semua registered users dan catat di database"""
        
        notification_type = (
            NotificationType.STNK_EXPIRY 
            if expiry_type == "STNK" 
            else NotificationType.KIR_EXPIRY
        )
        
        message = self.format_expiry_notification(
            vehicle, expiry_type, expiry_date, days_remaining
        )
        
        notification = TelegramNotification(
            notification_type=notification_type,
            vehicle_id=vehicle.id,
            message=message,
            is_sent=False
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        success = await self._send_to_all_users(db, message)
        
        notification.is_sent = success
        if success:
            notification.sent_at = datetime.utcnow()
        else:
            notification.error_message = "Gagal kirim alert expired"
            
        db.commit()
        return notification

    async def _send_to_all_users(self, db: Session, message: str) -> bool:
        """
        Kirim pesan ke semua registered Telegram users.
        Coba kirim ke semua yang aktif, return True jika minimal 1 berhasil.
        """
        # Ambil semua registered users
        registered_users = db.query(TelegramUser).filter(
            TelegramUser.is_active == True
        ).all()
        
        if not registered_users:
            logger.warning("⚠️ No registered Telegram users found. Skipping notification.")
            return False
        
        logger.info(f"📢 Sending notification to {len(registered_users)} registered users...")
        
        success_count = 0
        failed_count = 0
        
        for user in registered_users:
            try:
                sent = await self.send_message_to_chat_id(user.chat_id, message)
                
                if sent:
                    success_count += 1
                    user.last_notification_at = datetime.utcnow()
                    db.add(user)
                else:
                    failed_count += 1
                    # Mark as inactive jika failed beberapa kali (bisa di-enhance lebih lanjut)
                    logger.warning(f"⚠️ Failed to send to user {user.chat_id}")
                    
            except Exception as e:
                logger.error(f"❌ Error sending to {user.chat_id}: {str(e)}")
                failed_count += 1
        
        db.commit()
        
        logger.info(f"✅ Notification sent - Success: {success_count}/{len(registered_users)}, Failed: {failed_count}")
        
        # Return True jika minimal 1 user menerima notifikasi
        return success_count > 0

    async def register_user(self, db: Session, chat_id: str, first_name: str = None, last_name: str = None, username: str = None) -> TelegramUser:
        """
        Register atau update user Telegram yang sudah melakukan /start pada bot.
        Dipanggil ketika bot menerima /start command.
        """
        # Cek apakah user sudah terdaftar
        existing_user = db.query(TelegramUser).filter(
            TelegramUser.chat_id == str(chat_id)
        ).first()
        
        if existing_user:
            # Update data jika ada perubahan
            if first_name:
                existing_user.first_name = first_name
            if last_name:
                existing_user.last_name = last_name
            if username:
                existing_user.username = username
            existing_user.is_active = True
            
            logger.info(f"♻️ Updated Telegram user: {chat_id}")
            db.add(existing_user)
            db.commit()
            db.refresh(existing_user)
            return existing_user
        
        # Buat user baru
        new_user = TelegramUser(
            chat_id=str(chat_id),
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_active=True
        )
        
        logger.info(f"✅ Registered new Telegram user: {chat_id} - {first_name or username or 'Unknown'}")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    async def get_registered_users_count(self, db: Session) -> int:
        """Get total active registered users"""
        return db.query(TelegramUser).filter(
            TelegramUser.is_active == True
        ).count()

    async def close(self):
        """Close httpx client gracefully"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.info("🔌 Telegram client closed")

# Global instance
telegram_service = TelegramService()