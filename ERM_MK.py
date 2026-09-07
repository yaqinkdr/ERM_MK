import csv
import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Dictionary utama untuk menyimpan data pasien (key ID sekarang string 4 digit)
data_pasien = {}

# Dictionary untuk obat dari CSV
obat_dict = {}  # {nama_obat: harga}

# File CSV untuk menyimpan data
FILE_PASIEN = "pasien.csv"
FILE_REKAM_MEDIS = "rekam_medis.csv"
FILE_OBAT = "dataObat.csv"

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
            'Vitamin C': 3000
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

def load_data():
    """Memuat data dari CSV ke dictionary saat program dimulai."""
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
        with open(FILE_REKAM_MEDIS, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id_pasien = row['id_pasien']
                if id_pasien in data_pasien:
                    # Kompatibilitas dengan CSV lama
                    resep_list = eval(row.get('resep', '[]')) if row.get('resep') else []
                    total_harga = int(row.get('total_harga', '0')) if row.get('total_harga') else 0
                    subjective = row.get('subjective', row.get('diagnosis', ''))
                    objective = row.get('objective', '')
                    assessment = row.get('assessment', row.get('diagnosis', ''))
                    plan = row.get('plan', row.get('catatan', ''))
                    # Vital signs kompatibilitas
                    vital_signs = eval(row.get('vital_signs', '{}')) if row.get('vital_signs') else {}
                    if not vital_signs and 'vital_signs' in row and row['vital_signs']:
                        vital_signs = {'BP': row['vital_signs'], 'HR': '', 'T': '', 'RR': '', 'SpO2': ''}
                    if 'obat' in row and row['obat'] and not resep_list:
                        resep_list = [{'obat': row['obat'], 'jumlah': 1, 'harga': obat_dict.get(row['obat'], 0)}]
                        total_harga = obat_dict.get(row['obat'], 0)
                    data_pasien[id_pasien]['rekam_medis'].append({
                        'tanggal': row['tanggal'],
                        'subjective': subjective,
                        'objective': objective,
                        'vital_signs': vital_signs,
                        'assessment': assessment,
                        'plan': plan,
                        'resep': resep_list,
                        'total_harga': total_harga
                    })
    except FileNotFoundError:
        pass  # File belum ada, akan dibuat saat menyimpan

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
        fieldnames = ['id_pasien', 'tanggal', 'subjective', 'objective', 'vital_signs', 'assessment', 'plan', 'resep', 'total_harga']
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
                    'total_harga': rekam['total_harga']
                })

def generate_pdf(id_pasien):
    """Generate PDF rekam medis untuk pasien tertentu."""
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
        for rekam in info['rekam_medis']:
            vital = rekam['vital_signs']
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

def tambah_pasien_gui():
    """Membuat jendela untuk input data pasien."""
    window = tk.Toplevel()
    window.title("Tambah Pasien")
    window.geometry("400x300")

    tk.Label(window, text="Nama:").pack(pady=5)
    entry_nama = tk.Entry(window)
    entry_nama.pack(pady=5)

    tk.Label(window, text="Umur:").pack(pady=5)
    entry_umur = tk.Entry(window)
    entry_umur.pack(pady=5)

    tk.Label(window, text="Jenis Kelamin (L/P):").pack(pady=5)
    entry_jk = tk.Entry(window)
    entry_jk.pack(pady=5)

    def submit():
        try:
            nama = entry_nama.get()
            umur = int(entry_umur.get())
            jenis_kelamin = entry_jk.get().upper()
            if not nama or umur < 0 or jenis_kelamin not in ['L', 'P']:
                messagebox.showerror("Error", "Isi semua field dengan benar! (Jenis kelamin: L/P)")
                return
            id_pasien = f"{len(data_pasien) + 1:04d}"  # 4 digit dengan leading zero
            data_pasien[id_pasien] = {
                'nama': nama,
                'umur': umur,
                'jenis_kelamin': jenis_kelamin,
                'rekam_medis': []
            }
            save_pasien()
            messagebox.showinfo("Sukses", f"Pasien dengan ID {id_pasien} berhasil ditambahkan.")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Umur harus berupa angka!")

    tk.Button(window, text="Simpan", command=submit).pack(pady=20)
    tk.Button(window, text="Batal", command=window.destroy).pack(pady=5)

def tambah_rekam_medis_gui():
    """Membuat jendela untuk input rekam medis dengan grid layout 2 kolom."""
    window = tk.Toplevel()
    window.title("Tambah Rekam Medis")
    window.geometry("600x500")

    # Frame utama untuk grid
    frame = tk.Frame(window)
    frame.pack(pady=10, padx=10, fill='both')

    # Kolom kiri: ID Pasien dan SOAP
    frame_left = tk.Frame(frame)
    frame_left.grid(row=0, column=0, sticky='n', padx=5)

    tk.Label(frame_left, text="ID Pasien (4 digit):").pack(pady=5)
    entry_id = tk.Entry(frame_left)
    entry_id.pack(pady=5)

    tk.Label(frame_left, text="Subjective:").pack(pady=5)
    entry_subjective = tk.Entry(frame_left, width=30)
    entry_subjective.pack(pady=5)

    tk.Label(frame_left, text="Objective:").pack(pady=5)
    entry_objective = tk.Entry(frame_left, width=30)
    entry_objective.pack(pady=5)

    tk.Label(frame_left, text="Assessment:").pack(pady=5)
    entry_assessment = tk.Entry(frame_left, width=30)
    entry_assessment.pack(pady=5)

    tk.Label(frame_left, text="Plan:").pack(pady=5)
    entry_plan = tk.Entry(frame_left, width=30)
    entry_plan.pack(pady=5)

    # Kolom kanan: Vital Signs dan Resep
    frame_right = tk.Frame(frame)
    frame_right.grid(row=0, column=1, sticky='n', padx=5)

    # Frame Vital Signs
    frame_vital = tk.LabelFrame(frame_right, text="Vital Signs")
    frame_vital.pack(pady=5, fill='x')
    tk.Label(frame_vital, text="BP (e.g., 120/80):").grid(row=0, column=0, sticky='w', padx=5)
    entry_bp = tk.Entry(frame_vital, width=15)
    entry_bp.grid(row=0, column=1, pady=2)
    tk.Label(frame_vital, text="HR (e.g., 80 bpm):").grid(row=1, column=0, sticky='w', padx=5)
    entry_hr = tk.Entry(frame_vital, width=15)
    entry_hr.grid(row=1, column=1, pady=2)
    tk.Label(frame_vital, text="T (e.g., 36.5 C):").grid(row=2, column=0, sticky='w', padx=5)
    entry_t = tk.Entry(frame_vital, width=15)
    entry_t.grid(row=2, column=1, pady=2)
    tk.Label(frame_vital, text="RR (e.g., 16/min):").grid(row=3, column=0, sticky='w', padx=5)
    entry_rr = tk.Entry(frame_vital, width=15)
    entry_rr.grid(row=3, column=1, pady=2)
    tk.Label(frame_vital, text="SpO2 (e.g., 98%):").grid(row=4, column=0, sticky='w', padx=5)
    entry_spo2 = tk.Entry(frame_vital, width=15)
    entry_spo2.grid(row=4, column=1, pady=2)

    # Frame Resep
    frame_resep = tk.LabelFrame(frame_right, text="Resep Obat")
    frame_resep.pack(pady=5, fill='x')
    tk.Label(frame_resep, text="Cari Obat:").grid(row=0, column=0, sticky='w', padx=5)
    entry_search_obat = tk.Entry(frame_resep, width=15)
    entry_search_obat.grid(row=0, column=1, pady=5)
    tk.Label(frame_resep, text="Pilih Obat:").grid(row=1, column=0, sticky='w', padx=5)
    combo_obat = ttk.Combobox(frame_resep, values=list(obat_dict.keys()), width=12)
    combo_obat.grid(row=1, column=1, pady=5)
    tk.Label(frame_resep, text="Jumlah:").grid(row=2, column=0, sticky='w', padx=5)
    entry_jumlah = tk.Entry(frame_resep, width=15)
    entry_jumlah.grid(row=2, column=1, pady=5)

    def update_obat_list(event=None):
        search_term = entry_search_obat.get().lower()
        filtered = [obat for obat in obat_dict if search_term in obat.lower()]
        combo_obat['values'] = filtered
        if filtered:
            combo_obat.set(filtered[0])
        else:
            combo_obat.set('')

    entry_search_obat.bind("<KeyRelease>", update_obat_list)

    resep_list = []  # List sementara untuk resep {obat, jumlah, harga}
    listbox_resep = tk.Listbox(frame_resep, height=4, width=25)
    listbox_resep.grid(row=3, column=0, columnspan=2, pady=5)

    def tambah_obat():
        obat = combo_obat.get()
        try:
            jumlah = int(entry_jumlah.get())
            if obat not in obat_dict or jumlah <= 0:
                messagebox.showerror("Error", "Pilih obat valid dan jumlah > 0!")
                return
            harga = obat_dict[obat] * jumlah
            resep_item = {'obat': obat, 'jumlah': jumlah, 'harga': harga}
            resep_list.append(resep_item)
            listbox_resep.insert(tk.END, f"{obat} x {jumlah} = {harga}")
            update_total()
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus angka!")

    def hapus_obat():
        selected = listbox_resep.curselection()
        if selected:
            index = selected[0]
            del resep_list[index]
            listbox_resep.delete(index)
            update_total()
        else:
            messagebox.showwarning("Warning", "Pilih obat yang ingin dihapus!")

    tk.Button(frame_resep, text="Tambah Obat", command=tambah_obat).grid(row=4, column=0, pady=5)
    tk.Button(frame_resep, text="Hapus Obat", command=hapus_obat).grid(row=4, column=1, pady=5)

    label_total = tk.Label(frame_resep, text="Total Harga: 0")
    label_total.grid(row=5, column=0, columnspan=2, pady=5)

    def update_total():
        total = sum(item['harga'] for item in resep_list)
        label_total.config(text=f"Total Harga: {total}")
        return total

    # Tombol Simpan dan Batal di bawah
    frame_buttons = tk.Frame(window)
    frame_buttons.pack(pady=10)

    def submit():
        try:
            id_pasien = entry_id.get()
            if id_pasien not in data_pasien:
                messagebox.showerror("Error", "ID pasien tidak ditemukan!")
                return
            subjective = entry_subjective.get()
            objective = entry_objective.get()
            vital_signs = {
                'BP': entry_bp.get(),
                'HR': entry_hr.get(),
                'T': entry_t.get(),
                'RR': entry_rr.get(),
                'SpO2': entry_spo2.get()
            }
            assessment = entry_assessment.get()
            plan = entry_plan.get()
            if not subjective or not objective or not assessment or not plan:
                messagebox.showerror("Error", "Isi semua field SOAP!")
                return
            total_harga = update_total()
            tanggal = datetime.date.today().strftime("%Y-%m-%d")
            rekam = {
                'tanggal': tanggal,
                'subjective': subjective,
                'objective': objective,
                'vital_signs': vital_signs,
                'assessment': assessment,
                'plan': plan,
                'resep': resep_list,
                'total_harga': total_harga
            }
            data_pasien[id_pasien]['rekam_medis'].append(rekam)
            save_rekam_medis()
            messagebox.showinfo("Sukses", "Rekam medis berhasil ditambahkan.")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Input tidak valid!")

    tk.Button(frame_buttons, text="Simpan", command=submit).pack(side='left', padx=5)
    tk.Button(frame_buttons, text="Batal", command=window.destroy).pack(side='left', padx=5)

def lihat_daftar_pasien_gui():
    """Menampilkan daftar pasien dalam tabel dengan fitur search."""
    window = tk.Toplevel()
    window.title("Daftar Pasien")
    window.geometry("600x400")

    tk.Label(window, text="Cari Pasien (ID/Nama):").pack(pady=5)
    entry_search = tk.Entry(window)
    entry_search.pack(pady=5)

    tree = ttk.Treeview(window, columns=('ID', 'Nama', 'Umur', 'JK'), show='headings')
    tree.heading('ID', text='ID Pasien')
    tree.heading('Nama', text='Nama')
    tree.heading('Umur', text='Umur')
    tree.heading('JK', text='Jenis Kelamin')
    tree.pack(fill='both', expand=True)

    def update_list():
        search_term = entry_search.get().lower()
        tree.delete(*tree.get_children())
        if not data_pasien:
            messagebox.showinfo("Info", "Belum ada pasien terdaftar.")
        else:
            for id_pasien, info in data_pasien.items():
                if search_term in id_pasien.lower() or search_term in info['nama'].lower():
                    tree.insert('', 'end', values=(id_pasien, info['nama'], info['umur'], info['jenis_kelamin']))

    tk.Button(window, text="Cari", command=update_list).pack(pady=10)
    tk.Button(window, text="Tutup", command=window.destroy).pack(pady=10)

    # Tampilkan semua awalnya
    update_list()

def lihat_rekam_medis_gui():
    """Membuat jendela untuk memilih ID pasien dan menampilkan rekam medis."""
    window = tk.Toplevel()
    window.title("Lihat Rekam Medis")
    window.geometry("600x400")

    tk.Label(window, text="Masukkan ID Pasien (4 digit):").pack(pady=5)
    entry_id = tk.Entry(window)
    entry_id.pack(pady=5)

    def show_rekam():
        try:
            id_pasien = entry_id.get()
            if id_pasien not in data_pasien:
                messagebox.showerror("Error", "ID pasien tidak ditemukan!")
                return
            info = data_pasien[id_pasien]
            window_rekam = tk.Toplevel()
            window_rekam.title(f"Rekam Medis - {info['nama']}")
            window_rekam.geometry("900x500")

            tree = ttk.Treeview(window_rekam, columns=('Tanggal', 'Subjective', 'Objective', 'BP', 'HR', 'T', 'RR', 'SpO2', 'Assessment', 'Plan', 'Total Harga'), show='headings')
            tree.heading('Tanggal', text='Tanggal')
            tree.heading('Subjective', text='Subjective')
            tree.heading('Objective', text='Objective')
            tree.heading('BP', text='BP')
            tree.heading('HR', text='HR')
            tree.heading('T', text='T')
            tree.heading('RR', text='RR')
            tree.heading('SpO2', text='SpO2')
            tree.heading('Assessment', text='Assessment')
            tree.heading('Plan', text='Plan')
            tree.heading('Total Harga', text='Total Harga')
            tree.pack(fill='both', expand=True)

            if not info['rekam_medis']:
                messagebox.showinfo("Info", "Belum ada rekam medis.")
            else:
                for rekam in info['rekam_medis']:
                    vital = rekam['vital_signs']
                    tree.insert('', 'end', values=(
                        rekam['tanggal'],
                        rekam['subjective'],
                        rekam['objective'],
                        vital.get('BP', ''),
                        vital.get('HR', ''),
                        vital.get('T', ''),
                        vital.get('RR', ''),
                        vital.get('SpO2', ''),
                        rekam['assessment'],
                        rekam['plan'],
                        rekam['total_harga']
                    ))

            tk.Button(window_rekam, text="Cetak PDF", command=lambda: generate_pdf(id_pasien)).pack(pady=10)
            tk.Button(window_rekam, text="Tutup", command=window_rekam.destroy).pack(pady=10)
        except ValueError:
            messagebox.showerror("Error", "ID pasien harus berupa angka!")

    tk.Button(window, text="Tampilkan", command=show_rekam).pack(pady=10)
    tk.Button(window, text="Batal", command=window.destroy).pack(pady=5)

def main_gui():
    """Membuat jendela utama GUI."""
    load_obat()  # Muat data obat
    load_data()  # Muat data pasien dan rekam
    root = tk.Tk()
    root.title("E-Rekam Medis PP Miftahul Khoirot")
    root.geometry("400x500")

    # Judul utama - bold dan lebih besar
    tk.Label(root, text="E-Rekam Medis PP Miftahul Khoirot", 
             font=("Helvetica", 16, "bold")).pack(pady=20)

    # Subtitle
    tk.Label(root, text="Seksi Kesehatan Santri Putra - @yaqinkdr 2025", 
             font=("Helvetica", 10)).pack(pady=5)

    tk.Button(root, text="Tambah Pasien", command=tambah_pasien_gui, width=20).pack(pady=10)
    tk.Button(root, text="Tambah Rekam Medis", command=tambah_rekam_medis_gui, width=20).pack(pady=10)
    tk.Button(root, text="Lihat Daftar Pasien", command=lihat_daftar_pasien_gui, width=20).pack(pady=10)
    tk.Button(root, text="Lihat Rekam Medis", command=lihat_rekam_medis_gui, width=20).pack(pady=10)
    tk.Button(root, text="Keluar", command=root.quit, width=20).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
