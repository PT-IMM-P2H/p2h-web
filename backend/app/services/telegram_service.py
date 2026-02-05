from typing import Optional, List
import logging
import asyncio
from datetime import datetime
import httpx
from sqlalchemy.orm import Session

from app.config import settings
from app.models.notification import TelegramNotification, NotificationType
from app.models.vehicle import Vehicle
from app.models.p2h import P2HReport, InspectionStatus

logger = logging.getLogger(__name__)


class BroadcastResult:
    """Result class for broadcast operations"""
    def __init__(self, total_subscribers: int = 0, success_count: int = 0, 
                 failed_count: int = 0, failed_chat_ids: List[str] = None):
        self.total_subscribers = total_subscribers
        self.success_count = success_count
        self.failed_count = failed_count
        self.failed_chat_ids = failed_chat_ids or []


class TelegramService:
    """Service for sending Telegram notifications for P2H and Expiry Alerts - Multi User Support"""
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.default_chat_id = settings.TELEGRAM_CHAT_ID  # Fallback chat ID
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
    
    def _get_active_subscribers(self, db: Session) -> List[str]:
        """Mendapatkan daftar chat_id dari subscriber aktif"""
        from app.models.telegram_subscriber import TelegramSubscriber
        
        subscribers = db.query(TelegramSubscriber).filter(
            TelegramSubscriber.is_active == True
        ).all()
        
        chat_ids = [s.chat_id for s in subscribers]
        
        # Jika tidak ada subscriber, gunakan default chat_id dari config
        if not chat_ids and self.default_chat_id:
            logger.info("No active subscribers found, using default chat_id")
            chat_ids = [self.default_chat_id]
        
        return chat_ids
    
    async def send_message_to_chat(self, chat_id: str, message: str, max_retries: int = 3) -> bool:
        """Kirim pesan ke satu chat_id tertentu dengan retry mechanism"""
        client = self._get_client()
        
        for attempt in range(max_retries):
            try:
                logger.info(f"📤 Sending telegram message to {chat_id} (attempt {attempt + 1}/{max_retries})")
                
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
                    logger.info(f"✅ Telegram message sent successfully to {chat_id}")
                    return True
                elif response.status_code == 400:
                    # Bad request - tidak perlu retry
                    logger.error(f"❌ Telegram API Bad Request for {chat_id}: {response.text}")
                    return False
                elif response.status_code == 403:
                    # Bot blocked by user
                    logger.warning(f"⚠️ Bot blocked by user {chat_id}")
                    return False
                else:
                    logger.warning(f"⚠️ Telegram API returned {response.status_code} for {chat_id}: {response.text}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    return False
                    
            except httpx.TimeoutException as e:
                logger.warning(f"⏱️ Telegram request timeout for {chat_id} on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                logger.error(f"❌ All {max_retries} attempts timed out for {chat_id}")
                return False
                
            except httpx.NetworkError as e:
                logger.warning(f"🌐 Network error for {chat_id} on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                logger.error(f"❌ Network error after {max_retries} attempts for {chat_id}")
                return False
                
            except Exception as e:
                logger.error(f"❌ Unexpected error sending telegram to {chat_id}: {str(e)}", exc_info=True)
                return False
        
        return False
    
    async def send_message(self, message: str, max_retries: int = 3) -> bool:
        """Kirim pesan ke default chat_id (backward compatible)"""
        if not self.default_chat_id:
            logger.error("❌ No default chat_id configured")
            return False
        return await self.send_message_to_chat(self.default_chat_id, message, max_retries)
    
    async def send_to_all_subscribers(self, db: Session, message: str) -> BroadcastResult:
        """Kirim pesan ke semua subscriber aktif"""
        chat_ids = self._get_active_subscribers(db)
        
        result = BroadcastResult(total_subscribers=len(chat_ids))
        
        if not chat_ids:
            logger.warning("⚠️ No active subscribers to send message to")
            return result
        
        logger.info(f"📤 Broadcasting message to {len(chat_ids)} subscribers")
        
        # Update last_notified_at untuk subscriber yang berhasil
        from app.models.telegram_subscriber import TelegramSubscriber
        
        for chat_id in chat_ids:
            success = await self.send_message_to_chat(chat_id, message)
            if success:
                result.success_count += 1
                # Update last_notified_at
                subscriber = db.query(TelegramSubscriber).filter(
                    TelegramSubscriber.chat_id == chat_id
                ).first()
                if subscriber:
                    subscriber.last_notified_at = datetime.utcnow()
            else:
                result.failed_count += 1
                result.failed_chat_ids.append(chat_id)
            
            # Small delay untuk menghindari rate limiting
            await asyncio.sleep(0.1)
        
        db.commit()
        
        logger.info(f"✅ Broadcast complete: {result.success_count}/{result.total_subscribers} successful")
        return result
    
    async def broadcast_message(self, db: Session, message: str, parse_mode: str = "HTML") -> BroadcastResult:
        """Alias untuk send_to_all_subscribers dengan parse_mode"""
        return await self.send_to_all_subscribers(db, message)
    
    async def get_bot_info(self) -> dict:
        """Mendapatkan informasi bot"""
        client = self._get_client()
        try:
            response = await client.get(f"{self.base_url}/getMe")
            if response.status_code == 200:
                return response.json().get("result", {})
            return {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    async def set_webhook(self, webhook_url: str) -> bool:
        """Setup webhook URL untuk bot"""
        client = self._get_client()
        try:
            response = await client.post(
                f"{self.base_url}/setWebhook",
                json={"url": webhook_url}
            )
            if response.status_code == 200:
                logger.info(f"✅ Webhook set to: {webhook_url}")
                return True
            logger.error(f"❌ Failed to set webhook: {response.text}")
            return False
        except Exception as e:
            logger.error(f"❌ Error setting webhook: {str(e)}")
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
        """Kirim notifikasi P2H ke SEMUA SUBSCRIBER dan catat di tabel telegram_notifications"""
        
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
        
        # Kirim ke SEMUA SUBSCRIBER
        result = await self.send_to_all_subscribers(db, message)
        
        # Update status kirim berdasarkan hasil broadcast
        notification.is_sent = result.success_count > 0
        if result.success_count > 0:
            notification.sent_at = datetime.utcnow()
        
        if result.failed_count > 0:
            notification.error_message = f"Gagal kirim ke {result.failed_count} dari {result.total_subscribers} subscriber"
        
        db.commit()
        logger.info(f"📤 P2H notification sent to {result.success_count}/{result.total_subscribers} subscribers")
        return notification
    
    async def send_expiry_notification(
        self,
        db: Session,
        vehicle: Vehicle,
        expiry_type: str,
        expiry_date: datetime,
        days_remaining: int
    ) -> Optional[TelegramNotification]:
        """Kirim notifikasi Expired ke SEMUA SUBSCRIBER dan catat di database"""
        
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
        
        # Kirim ke SEMUA SUBSCRIBER
        result = await self.send_to_all_subscribers(db, message)
        
        # Update status kirim berdasarkan hasil broadcast
        notification.is_sent = result.success_count > 0
        if result.success_count > 0:
            notification.sent_at = datetime.utcnow()
        
        if result.failed_count > 0:
            notification.error_message = f"Gagal kirim ke {result.failed_count} dari {result.total_subscribers} subscriber"
            
        db.commit()
        logger.info(f"📤 Expiry notification sent to {result.success_count}/{result.total_subscribers} subscribers")
        return notification

    async def close(self):
        """Close httpx client gracefully"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.info("🔌 Telegram client closed")

# Global instance
telegram_service = TelegramService()