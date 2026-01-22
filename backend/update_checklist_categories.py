"""
Script untuk update section_name checklist templates yang masih menggunakan 'UMUM'
menjadi kategori yang lebih spesifik berdasarkan keywords di item_name
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import SessionLocal
from app.models.checklist import ChecklistTemplate

def update_checklist_categories():
    db = SessionLocal()
    
    # Mapping keywords ke kategori
    category_mapping = {
        "OLI & RADIATOR": ["oli mesin", "oli kopling", "air radiator", "oli stering", "radiator"],
        "REM": ["rem", "dpn/belakang", "rem tangan"],
        "LAMPU-LAMPU": ["lampu", "besar jauh", "reting", "sein", "belakang", "rotari", "mundur"],
        "RODA": ["roda", "ban", "cadangan", "tekanan angin", "alur ban"],
        "BODY KABIN": ["fender", "pintu", "atap", "jok", "lantai", "karet mounting", "body"],
        "TOOLS": ["dongkrak", "konci roda", "segitiga pengaman", "traffic cone", "ac"],
        "SURAT-SURAT": ["p3k", "stnk", "kir", "surat"],
        "OTHERS": ["sabuk pengaman", "spidometer", "klakson", "spion", "wiper", 
                   "alarem mundur", "radio komunikasi", "knalpot", "no lambung", "apar"]
    }
    
    try:
        # Ambil semua checklist dengan section_name UMUM atau NULL
        umum_items = db.query(ChecklistTemplate).filter(
            (ChecklistTemplate.section_name == "UMUM") | 
            (ChecklistTemplate.section_name == None)
        ).all()
        
        if not umum_items:
            print("✅ Tidak ada checklist dengan kategori UMUM yang perlu diupdate")
            return
        
        print(f"📋 Ditemukan {len(umum_items)} item dengan kategori UMUM")
        updated_count = 0
        
        for item in umum_items:
            item_name_lower = item.item_name.lower()
            
            # Cari kategori yang cocok berdasarkan keywords
            new_category = None
            for category, keywords in category_mapping.items():
                if any(keyword in item_name_lower for keyword in keywords):
                    new_category = category
                    break
            
            # Jika tidak ada kategori yang cocok, set ke OTHERS
            if new_category is None:
                new_category = "OTHERS"
            
            # Update kategori
            old_category = item.section_name or "NULL"
            item.section_name = new_category
            updated_count += 1
            
            print(f"  ✓ '{item.item_name[:50]}...' : {old_category} → {new_category}")
        
        db.commit()
        print(f"\n✅ Berhasil update {updated_count} item checklist")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🔄 Memulai update kategori checklist templates...\n")
    update_checklist_categories()
    print("\n🎉 Update selesai!")
