"""
Script untuk menambahkan subscriber awal melalui Railway API
"""
import asyncio
import httpx

# Configuration
API_BASE_URL = "https://p2h-web-production.up.railway.app"
INITIAL_CHAT_IDS = [
    {"chat_id": "5625212555", "full_name": "Admin 1", "notes": "Initial admin subscriber 1"},
    {"chat_id": "1778221644", "full_name": "Admin 2", "notes": "Initial admin subscriber 2"},
    {"chat_id": "377036145", "full_name": "Admin 3", "notes": "Initial admin subscriber 3"}
]

async def add_subscribers_via_api():
    """Tambahkan subscriber melalui API (butuh admin token)"""
    print("=" * 60)
    print("📱 ADDING TELEGRAM SUBSCRIBERS VIA API")
    print("=" * 60)
    
    print("ℹ️  Untuk menambahkan subscriber, Anda perlu login sebagai admin")
    print("ℹ️  dan menggunakan token untuk API call")
    print("\n🔑 Cara mendapatkan admin token:")
    print("1. Login ke https://p2h-web.vercel.app sebagai admin")
    print("2. Buka Developer Tools (F12)")
    print("3. Cek Application/Storage > Cookies > access_token")
    print("4. Copy token tersebut")
    
    token = input("\n📋 Masukkan admin token: ").strip()
    
    if not token:
        print("❌ Token tidak boleh kosong!")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        for subscriber_data in INITIAL_CHAT_IDS:
            try:
                print(f"\n📤 Adding subscriber {subscriber_data['chat_id']}...")
                
                response = await client.post(
                    f"{API_BASE_URL}/api/telegram/subscribers",
                    headers=headers,
                    json=subscriber_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Successfully added: {subscriber_data['full_name']}")
                elif response.status_code == 400:
                    # Already exists
                    result = response.json()
                    if "sudah terdaftar" in result.get("message", ""):
                        print(f"ℹ️  Already exists: {subscriber_data['full_name']}")
                    else:
                        print(f"❌ Error: {result}")
                else:
                    print(f"❌ HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Exception: {str(e)}")

async def test_broadcast():
    """Test broadcast message"""
    print("\n" + "=" * 60)
    print("📢 TEST BROADCAST MESSAGE")
    print("=" * 60)
    
    token = input("📋 Masukkan admin token untuk test broadcast: ").strip()
    
    if not token:
        print("❌ Token tidak boleh kosong!")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    broadcast_data = {
        "message": """
🎯 <b>TEST BROADCAST - MULTI USER</b>

Sistem notifikasi P2H PT. IMM sudah support multi-user!

<b>📋 Subscriber yang akan menerima notifikasi:</b>
• Chat ID: 5625212555
• Chat ID: 1778221644  
• Chat ID: 377036145

<b>🔔 Notifikasi otomatis untuk:</b>
• P2H Abnormal (Stop operasi)
• P2H Warning (Perlu perbaikan)
• Dokumen STNK/KIR expired

<i>Sistem P2H PT. IMM Bontang</i>
        """.strip()
    }
    
    async with httpx.AsyncClient() as client:
        try:
            print("📤 Sending broadcast...")
            response = await client.post(
                f"{API_BASE_URL}/api/telegram/broadcast",
                headers=headers,
                json=broadcast_data
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    payload = result.get("payload", {})
                    print(f"✅ Broadcast berhasil!")
                    print(f"   Total subscribers: {payload.get('total_subscribers', 0)}")
                    print(f"   Success: {payload.get('success_count', 0)}")
                    print(f"   Failed: {payload.get('failed_count', 0)}")
                else:
                    print(f"❌ Error: {result}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

async def main():
    """Main menu"""
    while True:
        print("\n" + "=" * 60)
        print("🤖 TELEGRAM MULTI-USER MANAGEMENT")
        print("=" * 60)
        print("1. Add initial subscribers via API")
        print("2. Test broadcast message")
        print("3. Exit")
        
        choice = input("\nPilih opsi (1-3): ").strip()
        
        if choice == "1":
            await add_subscribers_via_api()
        elif choice == "2":
            await test_broadcast()
        elif choice == "3":
            print("👋 Selesai!")
            break
        else:
            print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    asyncio.run(main())