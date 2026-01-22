"""
Debug script untuk melihat kenapa notifikasi telegram tidak terkirim
saat submit P2H dengan status WARNING/ABNORMAL
"""
import asyncio
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.p2h import P2HReport, InspectionStatus
from app.models.vehicle import Vehicle
from app.services.telegram_service import telegram_service
from uuid import UUID

async def main():
    db = SessionLocal()
    
    try:
        # Ambil laporan WARNING terbaru yang tidak ada notifikasi
        report_id = "4e1b32ed-860f-4379-acc6-74c5a5911ad9"
        
        print(f"🔍 Mengambil P2H Report: {report_id}")
        report = db.query(P2HReport).filter(P2HReport.id == UUID(report_id)).first()
        
        if not report:
            print("❌ Report tidak ditemukan!")
            return
        
        print(f"✅ Report ditemukan:")
        print(f"   Vehicle ID: {report.vehicle_id}")
        print(f"   Status: {report.overall_status}")
        print(f"   Date: {report.submission_date}")
        print(f"   Time: {report.submission_time}")
        
        # Ambil vehicle
        vehicle = db.query(Vehicle).filter(Vehicle.id == report.vehicle_id).first()
        
        if not vehicle:
            print("❌ Vehicle tidak ditemukan!")
            return
        
        print(f"✅ Vehicle ditemukan: {vehicle.no_lambung}")
        
        # Test kirim notifikasi
        print(f"\n📤 Mencoba kirim notifikasi Telegram...")
        
        notification = await telegram_service.send_p2h_notification(
            db, vehicle, report, report.overall_status
        )
        
        if notification:
            print(f"✅ Notification dibuat:")
            print(f"   ID: {notification.id}")
            print(f"   Type: {notification.notification_type}")
            print(f"   Sent: {notification.is_sent}")
            print(f"   Error: {notification.error_message}")
            print(f"\n📱 Pesan yang dikirim:")
            print(notification.message)
        else:
            print(f"❌ Notification tidak dibuat (mungkin status NORMAL)")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
