"""
Script untuk setup Telegram Bot Webhook.
Setelah bot sudah dibuat di @BotFather, jalankan script ini untuk setup webhook.

Jalankan: python setup_webhook.py <BOT_TOKEN> <WEBHOOK_URL>
Contoh: python setup_webhook.py 8452421112:AAFvXNHS... https://p2h.railway.app
"""
import asyncio
import sys
import httpx
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

async def setup_webhook(bot_token: str, webhook_url: str):
    """Setup webhook untuk Telegram Bot"""
    
    base_url = f"https://api.telegram.org/bot{bot_token}"
    
    print("=" * 70)
    print("🤖 TELEGRAM BOT WEBHOOK SETUP")
    print("=" * 70)
    
    print(f"\n📝 Configuration:")
    print(f"   Bot Token: {bot_token[:30]}...")
    print(f"   Webhook URL: {webhook_url}/api/telegram/webhook")
    
    # 1. Get Bot Info
    print("\n1️⃣ Getting bot information...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/getMe")
            bot_info = response.json()
            
            if bot_info.get("ok"):
                bot_data = bot_info.get("result", {})
                print(f"   ✅ Bot Name: @{bot_data.get('username')}")
                print(f"   ✅ Bot First Name: {bot_data.get('first_name')}")
                print(f"   ✅ Bot ID: {bot_data.get('id')}")
            else:
                print(f"   ❌ Error: {bot_info.get('description')}")
                return False
    except Exception as e:
        print(f"   ❌ Error getting bot info: {str(e)}")
        return False
    
    # 2. Check current webhook
    print("\n2️⃣ Checking current webhook configuration...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/getWebhookInfo")
            webhook_info = response.json()
            
            if webhook_info.get("ok"):
                webhook_data = webhook_info.get("result", {})
                current_url = webhook_data.get("url")
                
                if current_url:
                    print(f"   ℹ️  Current webhook: {current_url}")
                else:
                    print("   ℹ️  No webhook set (using polling)")
            else:
                print(f"   ⚠️  Could not get webhook info: {webhook_info.get('description')}")
    except Exception as e:
        print(f"   ⚠️  Error checking webhook: {str(e)}")
    
    # 3. Set webhook
    print(f"\n3️⃣ Setting webhook to {webhook_url}/api/telegram/webhook...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/setWebhook",
                json={
                    "url": f"{webhook_url}/api/telegram/webhook",
                    "drop_pending_updates": False  # Keep pending updates
                }
            )
            
            result = response.json()
            
            if result.get("ok"):
                print("   ✅ Webhook set successfully!")
                description = result.get("description", "")
                print(f"   ℹ️  {description}")
            else:
                print(f"   ❌ Error setting webhook: {result.get('description')}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error setting webhook: {str(e)}")
        return False
    
    # 4. Verify webhook
    print("\n4️⃣ Verifying webhook setup...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/getWebhookInfo")
            webhook_info = response.json()
            
            if webhook_info.get("ok"):
                webhook_data = webhook_info.get("result", {})
                set_url = webhook_data.get("url")
                pending_updates = webhook_data.get("pending_update_count", 0)
                
                print(f"   ✅ Webhook URL: {set_url}")
                print(f"   ℹ️  Pending updates: {pending_updates}")
                
                if set_url == f"{webhook_url}/api/telegram/webhook":
                    print("   ✅ Webhook configuration verified!")
                else:
                    print(f"   ⚠️  URL mismatch!")
                    return False
            else:
                print(f"   ❌ Verification failed: {webhook_info.get('description')}")
                return False
                
    except Exception as e:
        print(f"   ❌ Verification error: {str(e)}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ WEBHOOK SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\n📝 Next steps:")
    print("   1. Ensure backend is running and accessible from internet")
    print("   2. Make sure TELEGRAM_BOT_TOKEN is set in .env")
    print("   3. Run migration: alembic upgrade head")
    print("   4. User can now /start the bot and get registered")
    print("   5. All registered users will receive P2H notifications")
    print("\n💡 Test webhook:")
    print("   • User /start the bot in Telegram")
    print("   • Check database: SELECT * FROM telegram_users;")
    print("   • Send test: curl -X POST http://localhost:8000/api/telegram/test-message")
    print("\n" + "=" * 70)
    
    return True

async def main():
    """Main function"""
    if len(sys.argv) < 3:
        print("\n❌ Missing arguments!")
        print("\nUsage: python setup_webhook.py <BOT_TOKEN> <WEBHOOK_URL>")
        print("\nExample:")
        print("  python setup_webhook.py 8452421112:AAFvXNHS... https://p2h.railway.app")
        print("  python setup_webhook.py <token> http://localhost:8000  # local testing")
        print("\nWhere:")
        print("  <BOT_TOKEN>   = Token from @BotFather (format: 123456:ABC-DEF...)")
        print("  <WEBHOOK_URL> = Your domain/IP where backend is hosted")
        print("                  (without /api/telegram/webhook suffix)")
        sys.exit(1)
    
    bot_token = sys.argv[1]
    webhook_url = sys.argv[2].rstrip('/')  # Remove trailing slash
    
    # Validate token format
    if ':' not in bot_token:
        print("\n❌ Invalid bot token format!")
        print("Token should be: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
        sys.exit(1)
    
    # Validate URL
    if not webhook_url.startswith(('http://', 'https://')):
        print("\n❌ Invalid webhook URL!")
        print("URL should start with http:// or https://")
        sys.exit(1)
    
    print()
    success = await setup_webhook(bot_token, webhook_url)
    print()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
