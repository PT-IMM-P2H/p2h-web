"""
Script untuk mengirim ulang notifikasi Telegram 
untuk laporan WARNING/ABNORMAL yang belum mendapat notifikasi
"""
import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.p2h import P2HReport, InspectionStatus
from app.models.vehicle import Vehicle
from app.models.notification import TelegramNotification
from app.services.telegram_service import telegram_service
from uuid import UUID

async def main():
    db = SessionLocal()
    
    try:
        # Ambil semua laporan WARNING/ABNORMAL yang belum ada notifikasi
        reports = db.query(P2HReport).filter(
            P2HReport.overall_status.in_([InspectionStatus.WARNING, InspectionStatus.ABNORMAL])
        ).order_by(P2HReport.created_at.desc()).all()
        
        print(f"🔍 Ditemukan {len(reports)} laporan WARNING/ABNORMAL")
        
        # Cek yang belum punya notifikasi
        missing_notifications = []
        for report in reports:
            notification = db.query(TelegramNotification).filter(
                TelegramNotification.report_id == report.id
            ).first()
            
            if not notification:
                missing_notifications.append(report)
        
        print(f"⚠️ {len(missing_notifications)} laporan tidak punya notifikasi\n")
        
        if not missing_notifications:
            print("✅ Semua laporan sudah punya notifikasi!")
            return
        
        # Kirim notifikasi untuk yang missing
        for report in missing_notifications:
            vehicle = db.query(Vehicle).filter(Vehicle.id == report.vehicle_id).first()
            
            if not vehicle:
                print(f"❌ Skip report {report.id}: vehicle tidak ditemukan")
                continue
            
            print(f"📤 Mengirim notifikasi untuk:")
            print(f"   Report ID: {report.id}")
            print(f"   Vehicle: {vehicle.no_lambung}")
            print(f"   Status: {report.overall_status}")
            print(f"   Date: {report.submission_date} {report.submission_time}")
            
            notification = await telegram_service.send_p2h_notification(
                db, vehicle, report, report.overall_status
            )
            
            if notification and notification.is_sent:
                print(f"   ✅ Berhasil dikirim\n")
            else:
                error = notification.error_message if notification else "Unknown error"
                print(f"   ❌ Gagal: {error}\n")
        
        print("=" * 50)
        print("✅ Selesai mengirim notifikasi!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
