"""
Script untuk mengirim ulang notifikasi Telegram untuk data P2H
yang sudah ada dengan status WARNING/ABNORMAL tapi belum dapat notifikasi

Jalankan: python resend_missing_notifications.py
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal
from app.models.p2h import P2HReport, InspectionStatus
from app.models.notification import TelegramNotification
from app.services.telegram_service import telegram_service
from app.config import settings
from sqlalchemy.orm import joinedload

async def resend_missing_notifications():
    """Kirim ulang notifikasi untuk data yang terlewat"""
    db = SessionLocal()
    
    try:
        print("=" * 70)
        print("📤 RESENDING MISSING TELEGRAM NOTIFICATIONS")
        print("=" * 70)
        
        # Check if Telegram is configured
        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
            print("\n❌ TELEGRAM NOT CONFIGURED!")
            print("\n📝 Silakan setup Telegram terlebih dahulu:")
            print("   1. Edit file backend/.env")
            print("   2. Isi TELEGRAM_BOT_TOKEN dan TELEGRAM_CHAT_ID")
            print("   3. Jalankan: python setup_telegram.py untuk test")
            return
        
        print(f"\n✅ Telegram configured")
        print(f"   Bot Token: {settings.TELEGRAM_BOT_TOKEN[:20]}...")
        print(f"   Chat ID: {settings.TELEGRAM_CHAT_ID}")
        
        # Query P2H reports dengan status bermasalah yang belum punya notifikasi
        print("\n🔍 Mencari data P2H yang belum mendapat notifikasi...")
        
        reports_with_issues = db.query(P2HReport).options(
            joinedload(P2HReport.vehicle),
            joinedload(P2HReport.user),
            joinedload(P2HReport.details).joinedload(P2HReport.details.checklist_item)
        ).filter(
            P2HReport.overall_status.in_([InspectionStatus.WARNING, InspectionStatus.ABNORMAL])
        ).order_by(
            P2HReport.submission_date.desc(),
            P2HReport.submission_time.desc()
        ).all()
        
        # Filter yang belum punya notifikasi
        reports_without_notification = []
        for report in reports_with_issues:
            notification = db.query(TelegramNotification).filter(
                TelegramNotification.report_id == report.id
            ).first()
            
            if not notification:
                reports_without_notification.append(report)
        
        print(f"\n📊 Total P2H dengan WARNING/ABNORMAL: {len(reports_with_issues)}")
        print(f"   ⚠️ Belum dapat notifikasi: {len(reports_without_notification)}")
        
        if not reports_without_notification:
            print("\n✅ Semua data sudah mendapat notifikasi!")
            print("   Tidak ada yang perlu dikirim ulang.")
            return
        
        # Konfirmasi
        print("\n" + "=" * 70)
        print("📋 DATA YANG AKAN DIKIRIM NOTIFIKASINYA:")
        print("=" * 70)
        
        for i, report in enumerate(reports_without_notification, 1):
            status_emoji = "❌" if report.overall_status == InspectionStatus.ABNORMAL else "⚠️"
            print(f"{i}. {status_emoji} {report.vehicle.no_lambung} - {report.overall_status.value.upper()}")
            print(f"   Tanggal: {report.submission_date.strftime('%d %b %Y')} - Shift {report.shift_number}")
        
        print("\n" + "=" * 70)
        response = input(f"📤 Kirim {len(reports_without_notification)} notifikasi ke Telegram? (y/n): ")
        
        if response.lower() != 'y':
            print("\n❌ Dibatalkan oleh user")
            return
        
        # Send notifications
        print("\n📤 Mengirim notifikasi...\n")
        
        sent_count = 0
        failed_count = 0
        
        for i, report in enumerate(reports_without_notification, 1):
            print(f"[{i}/{len(reports_without_notification)}] Processing report {report.id}...")
            
            try:
                # Send notification
                notification = await telegram_service.send_p2h_notification(
                    db, 
                    report.vehicle, 
                    report, 
                    report.overall_status
                )
                
                if notification and notification.is_sent:
                    sent_count += 1
                    print(f"   ✅ Notifikasi terkirim untuk {report.vehicle.no_lambung}")
                else:
                    failed_count += 1
                    print(f"   ❌ Gagal kirim notifikasi untuk {report.vehicle.no_lambung}")
                
                # Small delay to avoid rate limiting
                if i < len(reports_without_notification):
                    await asyncio.sleep(1)
                    
            except Exception as e:
                failed_count += 1
                print(f"   ❌ Error: {str(e)}")
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 SUMMARY")
        print("=" * 70)
        print(f"✅ Berhasil dikirim: {sent_count}")
        print(f"❌ Gagal dikirim: {failed_count}")
        print(f"📊 Total diproses: {len(reports_without_notification)}")
        
        if sent_count > 0:
            print("\n🎉 Notifikasi berhasil dikirim!")
            print("📱 Silakan cek Telegram Anda untuk melihat notifikasi.")
        
        if failed_count > 0:
            print("\n⚠️ Ada notifikasi yang gagal dikirim.")
            print("💡 Tips:")
            print("   1. Cek koneksi internet")
            print("   2. Pastikan bot token dan chat ID benar")
            print("   3. Pastikan bot sudah di-start di chat")
            print("   4. Jalankan script ini lagi untuk retry")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        await telegram_service.close()
        db.close()

def main():
    """Main function"""
    print("\n🤖 Resend Missing Telegram Notifications\n")
    asyncio.run(resend_missing_notifications())
    print("\n")

if __name__ == "__main__":
    main()
