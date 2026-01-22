"""
Generate Excel templates for bulk upload
Run this script to create template files for users and vehicles
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
import os

# Create templates directory
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
os.makedirs(templates_dir, exist_ok=True)


def create_users_template():
    """Generate template for bulk user upload"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data Pengguna"
    
    # Headers
    headers = [
        "Email *",
        "Nama Lengkap *",
        "Nomor Telepon *",
        "Tanggal Lahir (YYYY-MM-DD)",
        "Role *",
        "Kategori *",
        "Department",
        "Position",
        "Work Status"
    ]
    
    # Style headers
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border
        ws.column_dimensions[cell.column_letter].width = 20
    
    # Data validation for Role
    role_validation = DataValidation(
        type="list",
        formula1='"superadmin,admin,user"',
        allow_blank=False
    )
    role_validation.error = 'Pilih salah satu: superadmin, admin, user'
    role_validation.errorTitle = 'Invalid Role'
    ws.add_data_validation(role_validation)
    role_validation.add(f'E2:E1000')  # Apply to Role column
    
    # Data validation for Kategori
    kategori_validation = DataValidation(
        type="list",
        formula1='"PT,Travel"',
        allow_blank=False
    )
    kategori_validation.error = 'Pilih salah satu: PT, Travel'
    kategori_validation.errorTitle = 'Invalid Kategori'
    ws.add_data_validation(kategori_validation)
    kategori_validation.add(f'F2:F1000')  # Apply to Kategori column
    
    # Sample data (hanya 1 baris kosong untuk user input)
    sample_data = [
        ["", "", "", "", "", "", "", "", ""]  # Empty row for user input
    ]
    
    for row_num, row_data in enumerate(sample_data, 2):
        for col_num, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.value = value
            cell.border = border
            # Highlight mandatory fields if empty
            if value == "" and "*" in headers[col_num - 1]:
                cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    # Set Nomor Telepon column (column C/3) as TEXT format to preserve leading zeros
    for row in range(2, 1001):  # Apply to all data rows
        cell = ws.cell(row=row, column=3)  # Column C = Nomor Telepon
        cell.number_format = '@'  # '@' means TEXT format in Excel
    
    # Freeze first row
    ws.freeze_panes = 'A2'
    
    # Add instructions sheet
    ws_inst = wb.create_sheet("Instruksi")
    instructions = [
        ["INSTRUKSI UPLOAD DATA PENGGUNA", ""],
        ["", ""],
        ["1. Format File:", ""],
        ["", "- Simpan file sebagai .xlsx (Excel)"],
        ["", "- Jangan ubah nama kolom header"],
        ["", ""],
        ["2. Kolom Wajib (*:", ""],
        ["", "- Email: Format email yang valid (contoh: user@example.com)"],
        ["", "- Nama Lengkap: Nama lengkap pengguna"],
        ["", "- Nomor Telepon: Langsung ketik angka dengan 0 di depan (contoh: 081234567890)"],
        ["", "  * PENTING: Kolom sudah diformat TEXT, TIDAK PERLU menambahkan tanda petik (')"],
        ["", "  * Cukup ketik: 081234567890 dan angka 0 tidak akan hilang"],
        ["", "- Role: Pilih dari dropdown (superadmin/admin/user)"],
        ["", "- Kategori: Pilih dari dropdown (PT/Travel)"],
        ["", ""],
        ["3. Kolom Opsional:", ""],
        ["", "- Tanggal Lahir: Format YYYY-MM-DD (contoh: 1990-01-15)"],
        ["", "- Department, Position, Work Status: Isi sesuai kebutuhan"],
        ["", ""],
        ["4. Catatan:", ""],
        ["", "- Baris dengan email duplikat akan dilewati"],
        ["", "- Baris dengan data invalid akan dilaporkan sebagai error"],
        ["", "- Password default: 'P@ssw0rd123' (user harus ganti saat login pertama)"],
        ["", ""],
        ["5. Contoh Data:", ""],
        ["", "Lihat sheet 'Data Pengguna' untuk contoh format yang benar"],
    ]
    
    for row_num, row_data in enumerate(instructions, 1):
        ws_inst.cell(row=row_num, column=1).value = row_data[0]
        ws_inst.cell(row=row_num, column=2).value = row_data[1]
        if row_num == 1:
            ws_inst.cell(row=row_num, column=1).font = Font(size=14, bold=True, color="4472C4")
    
    ws_inst.column_dimensions['A'].width = 25
    ws_inst.column_dimensions['B'].width = 60
    
    # Save file
    filepath = os.path.join(templates_dir, 'template_data_pengguna.xlsx')
    wb.save(filepath)
    print(f"✅ Template pengguna created: {filepath}")


def create_vehicles_template():
    """Generate template for bulk vehicle upload"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data Kendaraan"
    
    # Headers
    headers = [
        "Nomor Polisi *",
        "Nomor Lambung",
        "Tipe Kendaraan *",
        "Kategori *",
        "Tahun Pembuatan",
        "Tanggal Expired STNK (YYYY-MM-DD)",
        "Tanggal Expired KIR (YYYY-MM-DD)",
        "Shift Type *"
    ]
    
    # Style headers
    header_fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border
        ws.column_dimensions[cell.column_letter].width = 22
    
    # Data validation for Tipe Kendaraan (will be populated from database)
    type_validation = DataValidation(
        type="list",
        formula1='"Light Vehicle,Electric Vehicle,Double Cabin,Single Cabin,Bus,Ambulance,Fire Truck,Komando,Truk Sampah"',
        allow_blank=False
    )
    type_validation.error = 'Pilih dari daftar tipe kendaraan'
    type_validation.errorTitle = 'Invalid Tipe'
    ws.add_data_validation(type_validation)
    type_validation.add(f'C2:C1000')
    
    # Data validation for Kategori
    kategori_validation = DataValidation(
        type="list",
        formula1='"PT,Travel"',
        allow_blank=False
    )
    kategori_validation.error = 'Pilih salah satu: PT, Travel'
    kategori_validation.errorTitle = 'Invalid Kategori'
    ws.add_data_validation(kategori_validation)
    kategori_validation.add(f'D2:D1000')
    
    # Data validation for Shift Type
    shift_validation = DataValidation(
        type="list",
        formula1='"Shift 1,Shift 2"',
        allow_blank=False
    )
    shift_validation.error = 'Pilih salah satu: Shift 1, Shift 2'
    shift_validation.errorTitle = 'Invalid Shift'
    ws.add_data_validation(shift_validation)
    shift_validation.add(f'H2:H1000')
    
    # Sample data (hanya 1 baris kosong untuk user input)
    sample_data = [
        ["", "", "", "", "", "", "", ""]  # Empty row for user input
    ]
    
    for row_num, row_data in enumerate(sample_data, 2):
        for col_num, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.value = value
            cell.border = border
            # Highlight mandatory fields
            if value == "" and "*" in headers[col_num - 1]:
                cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    # Freeze first row
    ws.freeze_panes = 'A2'
    
    # Add instructions sheet
    ws_inst = wb.create_sheet("Instruksi")
    instructions = [
        ["INSTRUKSI UPLOAD DATA KENDARAAN", ""],
        ["", ""],
        ["1. Format File:", ""],
        ["", "- Simpan file sebagai .xlsx (Excel)"],
        ["", "- Jangan ubah nama kolom header"],
        ["", ""],
        ["2. Kolom Wajib (*:", ""],
        ["", "- Nomor Polisi: Format standar (contoh: KT 1234 AB)"],
        ["", "- Tipe Kendaraan: Pilih dari dropdown"],
        ["", "- Kategori: PT atau Travel"],
        ["", "- Shift Type: Shift 1 atau Shift 2"],
        ["", ""],
        ["3. Kolom Opsional:", ""],
        ["", "- Nomor Lambung: Nomor identifikasi internal"],
        ["", "- Tahun Pembuatan: Format 4 digit (contoh: 2020)"],
        ["", "- Tanggal Expired STNK/KIR: Format YYYY-MM-DD"],
        ["", ""],
        ["4. Catatan:", ""],
        ["", "- Nomor polisi yang duplikat akan dilewati"],
        ["", "- Baris dengan data invalid akan dilaporkan sebagai error"],
        ["", "- Tanggal expired akan digunakan untuk reminder otomatis"],
        ["", ""],
        ["5. Contoh Data:", ""],
        ["", "Lihat sheet 'Data Kendaraan' untuk contoh format yang benar"],
    ]
    
    for row_num, row_data in enumerate(instructions, 1):
        ws_inst.cell(row=row_num, column=1).value = row_data[0]
        ws_inst.cell(row=row_num, column=2).value = row_data[1]
        if row_num == 1:
            ws_inst.cell(row=row_num, column=1).font = Font(size=14, bold=True, color="70AD47")
    
    ws_inst.column_dimensions['A'].width = 30
    ws_inst.column_dimensions['B'].width = 60
    
    # Save file
    filepath = os.path.join(templates_dir, 'template_data_kendaraan.xlsx')
    wb.save(filepath)
    print(f"✅ Template kendaraan created: {filepath}")


if __name__ == "__main__":
    print("🔧 Generating Excel templates...")
    print("")
    create_users_template()
    create_vehicles_template()
    print("")
    print("✅ All templates generated successfully!")
    print(f"📁 Location: {os.path.join(os.path.dirname(__file__), 'templates')}")
