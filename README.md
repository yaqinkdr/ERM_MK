# E-Rekam Medis PP Miftahul Khoirot

Aplikasi desktop berbasis Python untuk mencatat rekam medis santri, dengan fitur SOAP, vital signs, resep obat, dan cetak PDF.

**Dibuat untuk:** Seksi Kesehatan Santri Putra - PP Miftahul Khoirot  
**Tahun:** 2025  
**Kontak:** @yaqinkdr

---

## Fitur Utama

- **Manajemen Pasien** (Tambah, Lihat, Cari berdasarkan ID/Nama)
- **Pencatatan Rekam Medis** dengan format:
  - **S**ubjective (keluhan pasien)
  - **O**bjective (hasil pemeriksaan fisik)
  - **A**ssessment (diagnosis)
  - **P**lan (tindakan lanjutan)
- **Vital Signs** (BP, HR, T, RR, SpO2)
- **Resep Obat**:
  - Pilih obat dari daftar (bisa dicari)
  - Atur jumlah
  - Hitung total harga otomatis
- **Cetak PDF** rekam medis per pasien
- **Penyimpanan data** dalam file CSV (portabel, bisa dibuka di Excel)

---

## Teknologi yang Digunakan

- Python 3.x
- Tkinter (GUI)
- ReportLab (PDF)
- CSV (penyimpanan data)

---

## Struktur File

| File | Fungsi |
|------|--------|
| `ERM_MK.py` | File utama program |
| `pasien.csv` | Data pasien (ID, nama, umur, JK) |
| `rekam_medis.csv` | Data rekam medis (SOAP, vital signs, resep, total harga) |
| `dataObat.csv` | Daftar obat dan harga |
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
1. Klik tombol **Tambah Pasien**
2. Isi nama, umur, dan jenis kelamin (L/P)
3. Klik **Simpan** → pasien mendapat ID 4 digit otomatis

### Menambahkan Rekam Medis
1. Klik tombol **Tambah Rekam Medis**
2. Masukkan **ID Pasien** (4 digit)
3. Isi **SOAP** (Subjective, Objective, Assessment, Plan)
4. Isi **Vital Signs** (opsional)
5. Tambahkan **Resep Obat**:
   - Ketik nama obat di kotak "Cari Obat" untuk filter
   - Pilih obat dari daftar
   - Masukkan jumlah
   - Klik **Tambah Obat** (akan muncul di daftar, total harga terupdate)
6. Klik **Simpan**

### Melihat Daftar Pasien
- Klik **Lihat Daftar Pasien**
- Gunakan kotak pencarian (cari ID atau nama)
- Klik **Cari** untuk filter

### Melihat & Cetak PDF Rekam Medis
1. Klik **Lihat Rekam Medis**
2. Masukkan ID pasien
3. Klik **Tampilkan** → muncul riwayat rekam medis dalam tabel
4. Klik **Cetak PDF** → file PDF `rekam_medis_[ID].pdf` dibuat di folder yang sama

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
- **Kompatibilitas mundur** untuk format data lama (vital signs, resep)
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
