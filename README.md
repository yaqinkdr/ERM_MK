# E-Rekam Medis PP Miftahul Khoirot

Aplikasi desktop berbasis Python untuk pencatatan rekam medis santri, dengan fitur SOAP, resep obat, upload hasil penunjang (format bebas), riwayat terstruktur, dan cetak PDF.

**Dibuat untuk:** Seksi Kesehatan Santri Putra - PP Miftahul Khoirot  
**Tahun:** 2025  
**Kontak:** @yaqinkdr

---

## Fitur Utama

- **Manajemen Pasien** (Tambah, Cari, Daftar)
- **Pencatatan Rekam Medis** dengan format SOAP:
  - **S**ubjective (keluhan)
  - **O**bjective (hasil pemeriksaan fisik)
  - **A**ssessment (diagnosis)
  - **P**lan (tindakan lanjutan)
- **Vital Signs** (BP, HR, T, RR, SpO2)
- **Resep Obat**:
  - Pilih dari daftar obat (bisa dicari)
  - Atur jumlah
  - Hitung total harga otomatis
- **Upload Hasil Penunjang** (format bebas):
  - PDF, JPG, PNG, DOCX, XLSX, TXT, ZIP, dll.
  - Tersimpan per pasien dengan timestamp
- **Riwayat Per Pasien**:
  - Urut dari terbaru ke lama
  - Tampilkan nama file penunjang
  - Buka file langsung dari aplikasi
- **Cetak PDF** rekam medis per pasien
- **Backup Manual** (sekali klik → zip semua data)
- **Penyimpanan data** dalam file CSV (portabel, bisa dibuka di Excel)

---

## Teknologi yang Digunakan

- Python 3.x
- Tkinter (GUI)
- ReportLab (PDF)
- CSV (penyimpanan data)
- ZIP (backup)

---

## Struktur File

| File/Folder | Fungsi |
|-------------|--------|
| `erm_pesantren_final.py` | File utama program |
| `pasien.csv` | Data pasien (ID, nama, umur, JK) |
| `rekam_medis.csv` | Data rekam medis (SOAP, vital signs, resep, file penunjang) |
| `dataObat.csv` | Daftar obat dan harga |
| `data/` | Folder penyimpanan file penunjang (terstruktur per ID pasien) |
| `backup/` | Folder hasil backup (dibuat otomatis saat backup) |
| `rekam_medis_[ID].pdf` | PDF rekam medis per pasien (dihasilkan saat cetak) |

---

## Cara Instalasi

### 1. Clone atau download repository ini

```bash
git clone https://github.com/[username]/e-rekam-medis.git
cd e-rekam-medis
```

### 2. Install dependensi

```bash
pip install reportlab
```

> **Catatan:** Tkinter biasanya sudah termasuk dalam instalasi Python standar. Jika belum, install sesuai sistem operasi Anda (misal: `sudo apt-get install python3-tk` di Linux).

### 3. Jalankan program

```bash
python ERM_MK.py
```

---

## Cara Penggunaan

### Menambahkan Pasien Baru
1. Buka tab **Daftar Pasien**
2. Klik **Tambah Pasien**
3. Isi nama, umur, dan jenis kelamin (L/P)
4. Klik **Simpan** → pasien mendapat ID 4 digit otomatis

### Menambahkan Rekam Medis
1. Buka tab **Rekam Medis**
2. Masukkan **ID Pasien** (4 digit) → klik **Cek** (muncul nama pasien)
3. Isi **SOAP** (Subjective, Objective, Assessment, Plan)
4. Isi **Vital Signs** (opsional)
5. Tambahkan **Resep Obat**:
   - Ketik nama obat di kotak "Cari Obat" untuk filter
   - Pilih obat dari daftar
   - Masukkan jumlah
   - Klik **Tambah Obat** (muncul di daftar, total harga terupdate)
6. Upload **Hasil Penunjang** (opsional):
   - Klik **Upload File**
   - Pilih file apapun (PDF, gambar, dokumen, dll.)
   - File tersimpan di folder `data/[ID_PASIEN]/`
7. Klik **Simpan Rekam Medis**

### Melihat Riwayat Pasien
1. Buka tab **Riwayat**
2. Masukkan ID pasien → klik **Tampilkan**
3. Semua entri rekam medis muncul (urut terbaru di atas)
4. Kolom **File** menampilkan nama file penunjang (jika ada)
5. Pilih entri → klik **Buka File Penunjang** untuk membuka file

### Cetak PDF
- Dari tab **Daftar Pasien**: pilih pasien → klik **Cetak PDF**
- Dari tab **Riwayat**: setelah tampilkan riwayat → klik **Cetak PDF**

### Backup Data
- Klik tombol **Backup Data (Manual)** di bagian bawah jendela
- Semua file CSV + folder `data/` di-zip ke folder `backup/` dengan timestamp
- Contoh: `backup_20250907_143022.zip`

---

## Manajemen Data Obat

File `dataObat.csv` berisi daftar obat dengan format:

```csv
nama_obat,harga
Paracetamol,5000
Amoxicillin,10000
Vitamin C,3000
```

- Jika file belum ada, program membuat contoh saat pertama kali dijalankan
- Anda bisa mengedit file `.csv` secara manual (dengan Excel/Notepad) untuk menambah/mengubah obat dan harga

---

## Catatan Teknis

- **ID Pasien** otomatis 4 digit dengan leading zero (misal: 0001, 0010, 0100)
- **Data tersimpan di CSV**, jadi mudah dicadangkan, dipindahkan, atau dibuka di spreadsheet lain
- **File penunjang** disimpan di `data/[ID_PASIEN]/[timestamp]_[nama_file]`
- **Riwayat** otomatis diurutkan dari tanggal terbaru ke terlama
- **Backup** bersifat manual (tidak otomatis) untuk menghemat ruang penyimpanan
- **Semua file CSV** menggunakan encoding UTF-8

---

## Kontribusi

Aplikasi ini dikembangkan khusus untuk kebutuhan PP Miftahul Khoirot. Jika ingin berkontribusi atau mengadaptasi untuk keperluan lain, silakan:

1. Fork repository
2. Buat branch fitur (`git checkout -b fitur-baru`)
3. Commit perubahan (`git commit -m 'Tambah fitur X'`)
4. Push ke branch (`git push origin fitur-baru`)
5. Buat Pull Request

---

## Lisensi

Hak Cipta © 2025 - @yaqinkdr

Aplikasi ini dibuat untuk penggunaan internal dan non-komersial. Silakan digunakan, dipelajari, dan dimodifikasi untuk kebutuhan pendidikan/kesehatan, dengan menyertakan kredit kepada penulis asli.

---

## Kontak

Untuk pertanyaan atau saran: **@yaqinkdr**

---

*Terima kasih telah menggunakan E-Rekam Medis PP Miftahul Khoirot. Semoga bermanfaat untuk pelayanan kesehatan santri.*
```
