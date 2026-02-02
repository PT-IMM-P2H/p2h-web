from datetime import datetime, date, time, timedelta
import pytz
from app.config import settings

def get_current_datetime() -> datetime:
    """Mendapatkan waktu sekarang sesuai timezone Asia/Makassar (WITA)"""
    tz = pytz.timezone(settings.TIMEZONE)
    return datetime.now(tz)

def get_current_date_shift() -> date:
    """
    [LOGIKA OPERASIONAL SHIFT - Kuning, Long Shift] 
    Reset jam 05:00 pagi.
    Jika waktu < 05:00 pagi, maka dianggap masih tanggal hari sebelumnya.
    """
    now = get_current_datetime()
    # Jika jam sekarang antara 00:00 sampai 04:59
    if now.hour < 5:
        return (now - timedelta(days=1)).date()
    return now.date()

def get_current_date_non_shift() -> date:
    """
    [LOGIKA OPERASIONAL NON-SHIFT - Hijau, Biru]
    Reset jam 00:00 (12 malam).
    Langsung menggunakan tanggal hari ini.
    """
    now = get_current_datetime()
    return now.date()

def get_current_date() -> date:
    """
    [DEPRECATED] Gunakan get_current_date_shift() atau get_current_date_non_shift()
    Fallback ke shift logic untuk backward compatibility.
    """
    return get_current_date_shift()

def get_current_time() -> time:
    """Mendapatkan jam sekarang (tanpa tanggal)"""
    return get_current_datetime().time()

def get_shift_number(current_time: time = None) -> int:
    """
    Menentukan shift berdasarkan jam kerja PT. IMM (Updated):
    - Shift 1: 07:00 - 15:00
    - Shift 2: 15:00 - 23:00
    - Shift 3: 23:00 - 07:00
    
    Toleransi mundur: 1 jam (bisa isi dari jam sebelumnya)
    """
    if current_time is None:
        current_time = get_current_time()
        
    now_hour = current_time.hour
    
    # Shift 1: 06:00 (toleransi -1 jam dari 07:00) sampai 15:00
    if 6 <= now_hour < 15:
        return 1
    # Shift 2: 14:00 (toleransi -1 jam dari 15:00) sampai 23:00
    elif 14 <= now_hour < 23:
        return 2
    # Shift 3: 22:00 (toleransi -1 jam dari 23:00) sampai 07:00
    else:
        return 3

def get_long_shift_number(current_time: time = None) -> int:
    """
    Menentukan long shift (2x sehari):
    - Long Shift 1: 07:00 - 19:00
    - Long Shift 2: 19:00 - 07:00
    
    Toleransi mundur: 1 jam
    """
    if current_time is None:
        current_time = get_current_time()
        
    now_hour = current_time.hour
    
    # Long Shift 1: 06:00 (toleransi -1 jam) sampai 19:00
    if 6 <= now_hour < 19:
        return 1
    # Long Shift 2: 18:00 (toleransi -1 jam) sampai 07:00
    else:
        return 2

def is_within_non_shift_hours(current_time: time = None) -> bool:
    """
    Cek apakah waktu saat ini dalam jam kerja non-shift.
    Non-shift (Hijau & Biru): 07:00 - 16:00
    Toleransi mundur: 1 jam (mulai dari 06:00)
    """
    if current_time is None:
        current_time = get_current_time()
        
    now_hour = current_time.hour
    
    # 06:00 (toleransi -1 jam dari 07:00) sampai 16:00
    return 6 <= now_hour < 16

def days_until_expiry(expiry_date: date) -> int:
    """
    [PENTING UNTUK SCHEDULER]
    Menghitung sisa hari menuju tanggal kadaluarsa (STNK/KIR).
    Digunakan oleh scheduler untuk mengirim alert ke Telegram.
    """
    if not expiry_date:
        return 999 # Jika tidak ada tanggal, dianggap masih lama
        
    today = get_current_date()
    delta = expiry_date - today
    return delta.days


def validate_shift_time(shift_number: int = None) -> tuple[bool, str]:
    """
    Validasi apakah shift_number yang dikirim sesuai dengan waktu saat ini.
    
    Shift numbers:
    - 0: Non-shift (hijau/biru) - bisa submit 06:00-16:00
    - 1, 2, 3: Regular shift (kuning)
    - 11, 12: Long shift
    
    Returns: (is_valid, error_message)
    """
    current_time = get_current_time()
    now_hour = current_time.hour
    
    # Jika shift_number None, backend akan auto-detect
    if shift_number is None:
        return True, ""
    
    # Non-shift (0)
    if shift_number == 0:
        if is_within_non_shift_hours(current_time):
            return True, ""
        else:
            return False, "Waktu submit untuk Non-Shift hanya 06:00-16:00"
    
    # Regular shift (1, 2, 3)
    if shift_number in [1, 2, 3]:
        expected_shift = get_shift_number(current_time)
        if shift_number == expected_shift:
            return True, ""
        else:
            return False, f"Shift {shift_number} tidak tersedia saat ini. Shift aktif: {expected_shift}"
    
    # Long shift (11, 12)
    if shift_number in [11, 12]:
        expected_long = get_long_shift_number(current_time)
        submitted_long = shift_number - 10  # Convert 11->1, 12->2
        if submitted_long == expected_long:
            return True, ""
        else:
            return False, f"Long Shift {submitted_long} tidak tersedia saat ini. Long Shift aktif: {expected_long}"
    
    # Unknown shift number
    return False, f"Shift number tidak valid: {shift_number}"
