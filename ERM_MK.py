"""
E-Rekam Medis PP Miftahul Khoirot - Final
Fitur:
- Manajemen pasien (tambah, cari, daftar)
- SOAP + Resep + Upload hasil penunjang per entri
- Riwayat per pasien (urut terbaru di atas, nama file ditampilkan)
- Cetak PDF
- Backup manual (tombol)
- Penyimpanan CSV

Dibuat untuk: Seksi Kesehatan Santri Putra - PP Miftahul Khoirot
Tahun: 2025
Kontak: @yaqinkdr
"""

import csv
import datetime
import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# ===================== KONFIGURASI =====================
FILE_PASIEN = "pasien.csv"
FILE_REKAM_MEDIS = "rekam_medis.csv"
DATA_FOLDER = "data"
FILE_OBAT = "dataObat.csv"
BACKUP_FOLDER = "backup"

# ===================== DATA OBAT =====================
obat_dict = {}  # {nama_obat: harga}

def load_obat():
    """Memuat data obat dari dataObat.csv."""
    global obat_dict
    try:
        with open(FILE_OBAT, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                obat_dict[row['nama_obat']] = int(row['harga'])
    except FileNotFoundError:
        # Buat contoh jika belum ada
        obat_dict = {
            'Paracetamol': 5000,
            'Amoxicillin': 10000,
            'Vitamin C': 3000,
            'Ibuprofen': 8000,
            'Cetirizine': 6000
        }
        save_obat()
        print(f"File {FILE_OBAT} dibuat dengan contoh data.")

def save_obat():
    """Menyimpan data obat ke dataObat.csv."""
    with open(FILE_OBAT, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['nama_obat', 'harga']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for nama, harga in obat_dict.items():
            writer.writerow({'nama_obat': nama, 'harga': harga})

# ===================== DATA PASIEN =====================
data_pasien = {}  # {id_pasien: {'nama':, 'umur':, 'jenis_kelamin':, 'rekam_medis': []}}

def load_data():
    """Memuat data dari CSV ke dictionary saat program dimulai."""
    global data_pasien
    data_pasien = {}
    
    # Load pasien
    try:
        with open(FILE_PASIEN, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id_pasien = row['id_pasien']
                data_pasien[id_pasien] = {
                    'nama': row['nama'],
                    'umur': int(row['umur']),
                    'jenis_kelamin': row['jenis_kelamin'],
                    'rekam_medis': []
                }
    except FileNotFoundError:
        pass
    
    # Load rekam medis
    try:
        with open(FILE_REKAM_MEDIS, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id_pasien = row['id_pasien']
                if id_pasien in data_pasien:
                    # Parse resep (format: [{'obat': 'Paracetamol', 'jumlah': 1, 'harga': 5000}])
                    resep_list = eval(row.get('resep', '[]')) if row.get('resep') else []
                    total_harga = int(row.get('total_harga', '0')) if row.get('total_harga') else 0
                    
                    # File penunjang (bisa kosong)
                    file_penunjang = row.get('file_penunjang', '')
                    
                    rekam = {
                        'tanggal': row['tanggal'],
                        'subjective': row.get('subjective', ''),
                        'objective': row.get('objective', ''),
                        'vital_signs': eval(row.get('vital_signs', '{}')) if row.get('vital_signs') else {},
                        'assessment': row.get('assessment', ''),
                        'plan': row.get('plan', ''),
                        'resep': resep_list,
                        'total_harga': total_harga,
                        'file_penunjang': file_penunjang
                    }
                    data_pasien[id_pasien]['rekam_medis'].append(rekam)
    except FileNotFoundError:
        pass

def save_pasien():
    """Menyimpan data pasien ke pasien.csv."""
    with open(FILE_PASIEN, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['id_pasien', 'nama', 'umur', 'jenis_kelamin']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for id_pasien, info in data_pasien.items():
            writer.writerow({
                'id_pasien': id_pasien,
                'nama': info['nama'],
                'umur': info['umur'],
                'jenis_kelamin': info['jenis_kelamin']
            })

def save_rekam_medis():
    """Menyimpan rekam medis ke rekam_medis.csv."""
    with open(FILE_REKAM_MEDIS, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['id_pasien', 'tanggal', 'subjective', 'objective', 
                     'vital_signs', 'assessment', 'plan', 'resep', 
                     'total_harga', 'file_penunjang']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for id_pasien, info in data_pasien.items():
            for rekam in info['rekam_medis']:
                writer.writerow({
                    'id_pasien': id_pasien,
                    'tanggal': rekam['tanggal'],
                    'subjective': rekam['subjective'],
                    'objective': rekam['objective'],
                    'vital_signs': str(rekam['vital_signs']),
                    'assessment': rekam['assessment'],
                    'plan': rekam['plan'],
                    'resep': str(rekam['resep']),
                    'total_harga': rekam['total_harga'],
                    'file_penunjang': rekam.get('file_penunjang', '')
                })

# ===================== BACKUP =====================
def backup_data():
    """Membuat backup semua data (CSV + folder data) ke folder backup/ dengan timestamp."""
    try:
        # Buat folder backup jika belum ada
        if not os.path.exists(BACKUP_FOLDER):
            os.makedirs(BACKUP_FOLDER)
        
        # Nama file backup: backup_2025-09-07_143022.zip
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.zip"
        backup_path = os.path.join(BACKUP_FOLDER, backup_name)
        
        # File yang akan di-backup
        files_to_backup = []
        for f in [FILE_PASIEN, FILE_REKAM_MEDIS, FILE_OBAT]:
            if os.path.exists(f):
                files_to_backup.append(f)
        
        # Tambahkan folder data/ (rekursif)
        if os.path.exists(DATA_FOLDER):
            for root, dirs, files in os.walk(DATA_FOLDER):
                for file in files:
                    files_to_backup.append(os.path.join(root, file))
        
        if not files_to_backup:
            messagebox.showwarning("Peringatan", "Tidak ada data yang bisa di-backup.")
            return
        
        # Buat zip
        import zipfile
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_backup:
                zipf.write(file, os.path.basename(file))
        
        messagebox.showinfo("Sukses", f"Backup berhasil dibuat:\n{backup_path}\n\nTotal {len(files_to_backup)} file.")
        
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuat backup:\n{e}")

# ===================== UTILITY =====================
def buka_file_eksternal(filepath):
    """Membuka file (PDF/Gambar) menggunakan program default OS."""
    if not filepath or not os.path.exists(filepath):
        messagebox.showerror("Error", f"File tidak ditemukan:\n{filepath}")
        return
    
    try:
        if sys.platform == "win32":
            os.startfile(filepath)
        elif sys.platform == "darwin":  # macOS
            os.system(f"open \"{filepath}\"")
        else:  # Linux
            os.system(f"xdg-open \"{filepath}\"")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuka file:\n{e}")

def generate_pdf(id_pasien):
    """Generate PDF rekam medis untuk pasien tertentu."""
    if id_pasien not in data_pasien:
        messagebox.showerror("Error", "ID pasien tidak ditemukan!")
        return
    
    info = data_pasien[id_pasien]
    pdf_file = f"rekam_medis_{id_pasien}.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"Rekam Medis Pasien {info['nama']} (ID: {id_pasien})", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Umur: {info['umur']}, Jenis Kelamin: {info['jenis_kelamin']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    if not info['rekam_medis']:
        elements.append(Paragraph("Belum ada rekam medis.", styles['Normal']))
    else:
        # Urutkan dari yang terbaru
        sorted_rekam = sorted(info['rekam_medis'], key=lambda x: x['tanggal'], reverse=True)
        for rekam in sorted_rekam:
            vital = rekam.get('vital_signs', {})
            data = [
                ["Tanggal:", rekam['tanggal']],
                ["Subjective:", rekam['subjective']],
                ["Objective:", rekam['objective']],
                ["Vital Signs:", ""],
                ["  BP:", vital.get('BP', '')],
                ["  HR:", vital.get('HR', '')],
                ["  T:", vital.get('T', '')],
                ["  RR:", vital.get('RR', '')],
                ["  SpO2:", vital.get('SpO2', '')],
                ["Assessment:", rekam['assessment']],
                ["Plan:", rekam['plan']],
                ["Resep:", ""]
            ]
            for item in rekam['resep']:
                data.append(["", f"{item['obat']} (jumlah: {item['jumlah']}, harga: {item['harga']})"])
            data.append(["Total Harga:", rekam['total_harga']])
            if rekam.get('file_penunjang'):
                data.append(["File Penunjang:", os.path.basename(rekam['file_penunjang'])])
            table = Table(data, colWidths=[100, 400])
            table.setStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10)
            ])
            elements.append(table)
            elements.append(Spacer(1, 24))

    doc.build(elements)
    messagebox.showinfo("Sukses", f"PDF berhasil dibuat: {pdf_file}")

# ===================== GUI UTAMA =====================
class ERMPesantrenApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Rekam Medis PP Miftahul Khoirot")
        self.geometry("1050x750")
        
        # Variabel untuk upload file sementara
        self.file_penunjang_temp = ''
        
        # Buat folder data jika belum ada
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)
        
        # Load data
        load_obat()
        load_data()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Notebook (tab)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")
        
        # Tab 1: Daftar Pasien
        tab_pasien = ttk.Frame(self.notebook)
        self.notebook.add(tab_pasien, text="📋 Daftar Pasien")
        self.setup_pasien_tab(tab_pasien)
        
        # Tab 2: Rekam Medis (SOAP + Upload)
        tab_rekam = ttk.Frame(self.notebook)
        self.notebook.add(tab_rekam, text="✏️ Rekam Medis")
        self.setup_rekam_tab(tab_rekam)
        
        # Tab 3: Riwayat
        tab_riwayat = ttk.Frame(self.notebook)
        self.notebook.add(tab_riwayat, text="📜 Riwayat")
        self.setup_riwayat_tab(tab_riwayat)
        
        # Tombol Backup di semua tab (letakkan di bawah notebook)
        backup_frame = ttk.Frame(self)
        backup_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(backup_frame, text="💾 Backup Data (Manual)", 
                  command=backup_data).pack(side="right", padx=5)
    
    # ==================== TAB PASIEN ====================
    def setup_pasien_tab(self, tab):
        frame = ttk.Frame(tab, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Tombol tambah pasien
        ttk.Button(frame, text="➕ Tambah Pasien", 
                  command=self.tambah_pasien_gui).pack(pady=5)
        
        # Pencarian
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill="x", pady=5)
        ttk.Label(search_frame, text="Cari (ID/Nama):").pack(side="left", padx=5)
        self.entry_search = ttk.Entry(search_frame, width=30)
        self.entry_search.pack(side="left", padx=5)
        ttk.Button(search_frame, text="🔍 Cari", 
                  command=self.update_pasien_list).pack(side="left", padx=5)
        
        # Treeview daftar pasien
        columns = ('ID', 'Nama', 'Umur', 'JK')
        self.tree_pasien = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree_pasien.heading(col, text=col)
            self.tree_pasien.column(col, width=100)
        self.tree_pasien.pack(fill="both", expand=True, pady=5)
        
        # Tombol aksi
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="📜 Lihat Riwayat", 
                  command=self.lihat_riwayat_dari_pasien).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📄 Cetak PDF", 
                  command=self.cetak_pdf_dari_pasien).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Refresh", 
                  command=self.update_pasien_list).pack(side="left", padx=5)
        
        # Tampilkan semua pasien
        self.update_pasien_list()
    
    def update_pasien_list(self):
        """Update daftar pasien di treeview"""
        search_term = self.entry_search.get().lower()
        self.tree_pasien.delete(*self.tree_pasien.get_children())
        
        if not data_pasien:
            return
        
        for id_pasien, info in data_pasien.items():
            if search_term in id_pasien.lower() or search_term in info['nama'].lower():
                self.tree_pasien.insert('', 'end', values=(
                    id_pasien, info['nama'], info['umur'], info['jenis_kelamin']
                ))
    
    def get_selected_pasien_id(self):
        """Mendapatkan ID pasien yang dipilih di treeview"""
        selection = self.tree_pasien.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih pasien terlebih dahulu!")
            return None
        return self.tree_pasien.item(selection[0])['values'][0]
    
    def lihat_riwayat_dari_pasien(self):
        """Buka tab riwayat untuk pasien yang dipilih"""
        id_pasien = self.get_selected_pasien_id()
        if id_pasien:
            self.notebook.select(2)  # Tab riwayat (index 2)
            self.tampilkan_riwayat(id_pasien)
    
    def cetak_pdf_dari_pasien(self):
        """Cetak PDF untuk pasien yang dipilih"""
        id_pasien = self.get_selected_pasien_id()
        if id_pasien:
            generate_pdf(id_pasien)
    
    # ==================== TAMBAH PASIEN ====================
    def tambah_pasien_gui(self):
        """Membuat jendela untuk input data pasien."""
        window = tk.Toplevel(self)
        window.title("Tambah Pasien")
        window.geometry("400x300")
        window.transient(self)
        window.grab_set()

        ttk.Label(window, text="Nama:").pack(pady=5)
        entry_nama = ttk.Entry(window, width=30)
        entry_nama.pack(pady=5)

        ttk.Label(window, text="Umur:").pack(pady=5)
        entry_umur = ttk.Entry(window, width=30)
        entry_umur.pack(pady=5)

        ttk.Label(window, text="Jenis Kelamin (L/P):").pack(pady=5)
        entry_jk = ttk.Entry(window, width=30)
        entry_jk.pack(pady=5)

        def submit():
            try:
                nama = entry_nama.get().strip()
                umur = int(entry_umur.get())
                jenis_kelamin = entry_jk.get().upper().strip()
                if not nama or umur < 0 or jenis_kelamin not in ['L', 'P']:
                    messagebox.showerror("Error", "Isi semua field dengan benar! (Jenis kelamin: L/P)")
                    return
                # Generate ID (4 digit, auto increment)
                if data_pasien:
                    max_id = max(int(id) for id in data_pasien.keys())
                    id_pasien = f"{max_id + 1:04d}"
                else:
                    id_pasien = "0001"
                
                data_pasien[id_pasien] = {
                    'nama': nama,
                    'umur': umur,
                    'jenis_kelamin': jenis_kelamin,
                    'rekam_medis': []
                }
                save_pasien()
                messagebox.showinfo("Sukses", f"Pasien dengan ID {id_pasien} berhasil ditambahkan.")
                window.destroy()
                self.update_pasien_list()
            except ValueError:
                messagebox.showerror("Error", "Umur harus berupa angka!")

        ttk.Button(window, text="Simpan", command=submit).pack(pady=20)
        ttk.Button(window, text="Batal", command=window.destroy).pack(pady=5)
    
    # ==================== TAB REKAM MEDIS ====================
    def setup_rekam_tab(self, tab):
        # === MAIN FRAME dengan Scrollbar ===
        main_container = ttk.Frame(tab)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Canvas + Scrollbar
        canvas = tk.Canvas(main_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # === Semua komponen dimasukkan ke scrollable_frame ===
        # ID Pasien
        id_frame = ttk.Frame(scrollable_frame)
        id_frame.pack(fill="x", pady=5)
        ttk.Label(id_frame, text="ID Pasien:").pack(side="left", padx=5)
        self.entry_id_rekam = ttk.Entry(id_frame, width=15)
        self.entry_id_rekam.pack(side="left", padx=5)
        ttk.Button(id_frame, text="🔍 Cek", command=self.cek_pasien_rekam).pack(side="left", padx=5)
        self.label_nama_rekam = ttk.Label(id_frame, text="")
        self.label_nama_rekam.pack(side="left", padx=10)
        
        # SOAP
        soap_frame = ttk.LabelFrame(scrollable_frame, text="SOAP", padding="10")
        soap_frame.pack(fill="x", pady=5)
        
        soap_labels = ["Subjective:", "Objective:", "Assessment:", "Plan:"]
        self.soap_texts = {}
        for i, label_text in enumerate(soap_labels):
            ttk.Label(soap_frame, text=label_text).grid(row=i, column=0, padx=5, pady=4, sticky="nw")
            text_widget = tk.Text(soap_frame, height=3, width=70, wrap="word")
            text_widget.grid(row=i, column=1, padx=5, pady=5, sticky="nsew")
            self.soap_texts[label_text[:-1]] = text_widget
        soap_frame.grid_columnconfigure(1, weight=1)
        
        # Vital Signs
        vital_frame = ttk.LabelFrame(scrollable_frame, text="Vital Signs", padding="10")
        vital_frame.pack(fill="x", pady=5)
        
        vital_fields = ['BP', 'HR', 'T', 'RR', 'SpO2']
        self.vital_entries = {}
        for i, field in enumerate(vital_fields):
            ttk.Label(vital_frame, text=f"{field}:").grid(row=0, column=i*2, padx=5, pady=2)
            entry = ttk.Entry(vital_frame, width=12)
            entry.grid(row=0, column=i*2+1, padx=5, pady=2)
            self.vital_entries[field] = entry
        
        # Resep
        resep_frame = ttk.LabelFrame(scrollable_frame, text="Resep Obat", padding="10")
        resep_frame.pack(fill="x", pady=5)
        
        search_obat_frame = ttk.Frame(resep_frame)
        search_obat_frame.pack(fill="x", pady=2)
        ttk.Label(search_obat_frame, text="Cari Obat:").pack(side="left", padx=5)
        self.entry_search_obat = ttk.Entry(search_obat_frame, width=20)
        self.entry_search_obat.pack(side="left", padx=5)
        self.entry_search_obat.bind("<KeyRelease>", self.update_obat_list)
        
        obat_input_frame = ttk.Frame(resep_frame)
        obat_input_frame.pack(fill="x", pady=2)
        ttk.Label(obat_input_frame, text="Pilih Obat:").pack(side="left", padx=5)
        self.combo_obat = ttk.Combobox(obat_input_frame, values=list(obat_dict.keys()), width=20)
        self.combo_obat.pack(side="left", padx=5)
        ttk.Label(obat_input_frame, text="Jumlah:").pack(side="left", padx=5)
        self.entry_jumlah = ttk.Entry(obat_input_frame, width=5)
        self.entry_jumlah.pack(side="left", padx=5)
        ttk.Button(obat_input_frame, text="➕ Tambah", command=self.tambah_obat).pack(side="left", padx=5)
        
        self.listbox_resep = tk.Listbox(resep_frame, height=4)
        self.listbox_resep.pack(fill="x", pady=5)
        
        resep_btn_frame = ttk.Frame(resep_frame)
        resep_btn_frame.pack(fill="x", pady=2)
        ttk.Button(resep_btn_frame, text="❌ Hapus Obat", command=self.hapus_obat).pack(side="left", padx=5)
        self.label_total = ttk.Label(resep_btn_frame, text="Total Harga: 0")
        self.label_total.pack(side="right", padx=10)
        self.resep_list = []
        
        # Upload Penunjang
        upload_frame = ttk.LabelFrame(scrollable_frame, text="Hasil Penunjang", padding="10")
        upload_frame.pack(fill="x", pady=5)
        
        ttk.Button(upload_frame, text="📎 Upload File Penunjang", command=self.upload_penunjang).pack(side="left", padx=5)
        self.label_file_penunjang = ttk.Label(upload_frame, text="Belum ada file")
        self.label_file_penunjang.pack(side="left", padx=10)
        
        # Tombol Simpan
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="💾 SIMPAN Rekam Medis", command=self.simpan_rekam_medis).pack(pady=5)
        
        # === Posisi Canvas dan Scrollbar ===
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def cek_pasien_rekam(self):
        """Cek pasien berdasarkan ID untuk tab rekam medis"""
        id_pasien = self.entry_id_rekam.get().strip()
        if id_pasien in data_pasien:
            self.label_nama_rekam.config(
                text=f"{data_pasien[id_pasien]['nama']} ({data_pasien[id_pasien]['umur']} th, {data_pasien[id_pasien]['jenis_kelamin']})"
            )
        else:
            self.label_nama_rekam.config(text="❌ ID tidak ditemukan")
    
    def update_obat_list(self, event=None):
        """Filter daftar obat berdasarkan pencarian"""
        search_term = self.entry_search_obat.get().lower()
        filtered = [obat for obat in obat_dict if search_term in obat.lower()]
        self.combo_obat['values'] = filtered
        if filtered:
            self.combo_obat.set(filtered[0])
        else:
            self.combo_obat.set('')
    
    def tambah_obat(self):
        """Tambah obat ke daftar resep"""
        obat = self.combo_obat.get()
        try:
            jumlah = int(self.entry_jumlah.get())
            if obat not in obat_dict or jumlah <= 0:
                messagebox.showerror("Error", "Pilih obat valid dan jumlah > 0!")
                return
            harga = obat_dict[obat] * jumlah
            resep_item = {'obat': obat, 'jumlah': jumlah, 'harga': harga}
            self.resep_list.append(resep_item)
            self.listbox_resep.insert(tk.END, f"{obat} x {jumlah} = Rp{harga:,}")
            self.update_total()
            self.entry_jumlah.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus angka!")
    
    def hapus_obat(self):
        """Hapus obat yang dipilih dari daftar resep"""
        selected = self.listbox_resep.curselection()
        if selected:
            index = selected[0]
            del self.resep_list[index]
            self.listbox_resep.delete(index)
            self.update_total()
        else:
            messagebox.showwarning("Warning", "Pilih obat yang ingin dihapus!")
    
    def update_total(self):
        """Update total harga resep"""
        total = sum(item['harga'] for item in self.resep_list)
        self.label_total.config(text=f"Total Harga: Rp{total:,}")
        return total
    def upload_penunjang(self):
        """Upload file hasil penunjang (bebas format)"""
        id_pasien = self.entry_id_rekam.get().strip()
        if not id_pasien:
            messagebox.showwarning("Peringatan", "Isi ID Pasien dulu.")
            return
        if id_pasien not in data_pasien:
            messagebox.showerror("Error", "ID Pasien tidak ditemukan!")
            return
        
        # Filetypes dihapus → semua file bisa dipilih
        file_path = filedialog.askopenfilename(
            title="Pilih File Hasil Penunjang"
            # Tidak ada filetypes → semua file (*.*) bisa dipilih
        )
        if not file_path:
            return
        
        # Buat folder per pasien
        target_dir = os.path.join(DATA_FOLDER, id_pasien)
        os.makedirs(target_dir, exist_ok=True)
        
        # Simpan dengan timestamp agar unik
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = os.path.splitext(file_path)[1]
        new_filename = f"{timestamp}_{os.path.basename(file_path)}"
        target_path = os.path.join(target_dir, new_filename)
        
        try:
            shutil.copy2(file_path, target_path)
            self.file_penunjang_temp = target_path
            self.label_file_penunjang.config(text=f"✅ {os.path.basename(target_path)}")
            messagebox.showinfo("Berhasil", f"File disimpan sebagai:\n{target_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan file:\n{e}")
    
    def simpan_rekam_medis(self):
        """Simpan rekam medis ke CSV"""
        id_pasien = self.entry_id_rekam.get().strip()
        if not id_pasien:
            messagebox.showwarning("Peringatan", "ID Pasien tidak boleh kosong!")
            return
        if id_pasien not in data_pasien:
            messagebox.showerror("Error", "ID Pasien tidak ditemukan!")
            return
        
        # Kumpulkan data
        subjective = self.soap_texts['Subjective'].get("1.0", tk.END).strip()
        objective = self.soap_texts['Objective'].get("1.0", tk.END).strip()
        assessment = self.soap_texts['Assessment'].get("1.0", tk.END).strip()
        plan = self.soap_texts['Plan'].get("1.0", tk.END).strip()
        
        if not subjective or not objective or not assessment or not plan:
            messagebox.showerror("Error", "Isi semua field SOAP!")
            return
        
        # Vital signs
        vital_signs = {
            'BP': self.vital_entries['BP'].get().strip(),
            'HR': self.vital_entries['HR'].get().strip(),
            'T': self.vital_entries['T'].get().strip(),
            'RR': self.vital_entries['RR'].get().strip(),
            'SpO2': self.vital_entries['SpO2'].get().strip()
        }
        
        # Total harga
        total_harga = self.update_total()
        
        # File penunjang
        file_penunjang = getattr(self, 'file_penunjang_temp', '')
        
        tanggal = datetime.date.today().strftime("%Y-%m-%d")
        
        rekam = {
            'tanggal': tanggal,
            'subjective': subjective,
            'objective': objective,
            'vital_signs': vital_signs,
            'assessment': assessment,
            'plan': plan,
            'resep': self.resep_list.copy(),
            'total_harga': total_harga,
            'file_penunjang': file_penunjang
        }
        
        data_pasien[id_pasien]['rekam_medis'].append(rekam)
        save_rekam_medis()
        
        # Reset form
        for widget in self.soap_texts.values():
            widget.delete("1.0", tk.END)
        for entry in self.vital_entries.values():
            entry.delete(0, tk.END)
        self.resep_list = []
        self.listbox_resep.delete(0, tk.END)
        self.label_total.config(text="Total Harga: 0")
        self.file_penunjang_temp = ''
        self.label_file_penunjang.config(text="Belum ada file")
        
        messagebox.showinfo("Sukses", f"Rekam medis untuk ID {id_pasien} berhasil disimpan.")
    
    # ==================== TAB RIWAYAT ====================
    def setup_riwayat_tab(self, tab):
        frame = ttk.Frame(tab, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Input ID
        id_frame = ttk.Frame(frame)
        id_frame.pack(fill="x", pady=5)
        ttk.Label(id_frame, text="ID Pasien:").pack(side="left", padx=5)
        self.entry_id_riwayat = ttk.Entry(id_frame, width=15)
        self.entry_id_riwayat.pack(side="left", padx=5)
        ttk.Button(id_frame, text="🔍 Tampilkan", 
                  command=self.tampilkan_riwayat_from_entry).pack(side="left", padx=5)
        ttk.Button(id_frame, text="📄 Cetak PDF", 
                  command=self.cetak_pdf_riwayat).pack(side="left", padx=5)
        self.label_nama_riwayat = ttk.Label(id_frame, text="")
        self.label_nama_riwayat.pack(side="left", padx=10)
        
        # Treeview riwayat
        columns = ('Tanggal', 'Subjective', 'Objective', 'Assessment', 'Plan', 'File')
        self.tree_riwayat = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree_riwayat.heading(col, text=col)
            if col == 'File':
                self.tree_riwayat.column(col, width=200)
            else:
                self.tree_riwayat.column(col, width=130)
        self.tree_riwayat.pack(fill="both", expand=True, pady=5)
        
        # Tombol aksi
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="📎 Buka File Penunjang", 
                  command=self.buka_file_riwayat).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Refresh", 
                  command=self.refresh_riwayat).pack(side="left", padx=5)
    
    def tampilkan_riwayat_from_entry(self):
        """Tampilkan riwayat berdasarkan input ID di tab riwayat"""
        id_pasien = self.entry_id_riwayat.get().strip()
        self.tampilkan_riwayat(id_pasien)
    
    def tampilkan_riwayat(self, id_pasien):
        """Tampilkan riwayat pasien di treeview (urut terbaru di atas)"""
        self.tree_riwayat.delete(*self.tree_riwayat.get_children())
        
        if id_pasien not in data_pasien:
            self.label_nama_riwayat.config(text="❌ ID tidak ditemukan")
            return
        
        info = data_pasien[id_pasien]
        self.label_nama_riwayat.config(
            text=f"{info['nama']} ({info['umur']} th, {info['jenis_kelamin']})"
        )
        self.entry_id_riwayat.delete(0, tk.END)
        self.entry_id_riwayat.insert(0, id_pasien)
        
        if not info['rekam_medis']:
            messagebox.showinfo("Info", "Belum ada rekam medis untuk pasien ini.")
            return
        
        # Sortir dari yang terbaru
        sorted_rekam = sorted(info['rekam_medis'], key=lambda x: x['tanggal'], reverse=True)
        for rekam in sorted_rekam:
            # Tampilkan nama file (basename) atau "-" jika kosong
            file_display = os.path.basename(rekam.get('file_penunjang', '')) if rekam.get('file_penunjang') else "-"
            
            self.tree_riwayat.insert('', 'end', values=(
                rekam['tanggal'],
                rekam['subjective'][:40] + "..." if len(rekam['subjective']) > 40 else rekam['subjective'],
                rekam['objective'][:40] + "..." if len(rekam['objective']) > 40 else rekam['objective'],
                rekam['assessment'][:40] + "..." if len(rekam['assessment']) > 40 else rekam['assessment'],
                rekam['plan'][:40] + "..." if len(rekam['plan']) > 40 else rekam['plan'],
                file_display
            ))
        
        # Simpan ID pasien untuk aksi selanjutnya
        self.riwayat_current_id = id_pasien
        # Simpan daftar rekam yang sudah di-sort untuk mapping saat buka file
        self.riwayat_sorted_rekam = sorted_rekam
    
    def refresh_riwayat(self):
        """Refresh riwayat yang sedang ditampilkan"""
        if hasattr(self, 'riwayat_current_id'):
            self.tampilkan_riwayat(self.riwayat_current_id)
    
    def buka_file_riwayat(self):
        """Buka file penunjang dari riwayat yang dipilih"""
        selection = self.tree_riwayat.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih entri riwayat terlebih dahulu!")
            return
        
        if not hasattr(self, 'riwayat_sorted_rekam'):
            return
        
        # Dapatkan indeks entri yang dipilih
        index = self.tree_riwayat.index(selection[0])
        if index >= len(self.riwayat_sorted_rekam):
            return
        
        rekam = self.riwayat_sorted_rekam[index]
        file_path = rekam.get('file_penunjang', '')
        
        if not file_path:
            messagebox.showinfo("Info", "Entri ini tidak memiliki file penunjang.")
            return
        
        buka_file_eksternal(file_path)
    
    def cetak_pdf_riwayat(self):
        """Cetak PDF untuk pasien yang sedang dilihat riwayatnya"""
        id_pasien = self.entry_id_riwayat.get().strip()
        if id_pasien in data_pasien:
            generate_pdf(id_pasien)
        else:
            messagebox.showerror("Error", "ID pasien tidak ditemukan!")

# ===================== MAIN =====================
if __name__ == "__main__":
    # Buat folder data jika belum ada
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    
    app = ERMPesantrenApp()
    app.mainloop()
