# Sistem Pengelolaan Data Mahasiswa (CLI)

Aplikasi command line berbasis Python untuk UTS Pemrograman Dasar.

## Deskripsi dan Tujuan
Mengelola data mahasiswa secara sederhana: menampilkan, mencari, memfilter, menambah, menghapus, dan membuat rekapitulasi. Setiap mahasiswa punya nilai tugas, UTS, dan UAS; program menghitung nilai akhir, grade, dan status kelulusan otomatis.

## Target Pengguna
Mahasiswa atau petugas administrasi yang membutuhkan pengelolaan data mahasiswa sederhana.

## Fitur Utama
1. Tampilkan seluruh data mahasiswa
2. Cari mahasiswa berdasarkan NIM
3. Filter mahasiswa berdasarkan kelas (kelas bebas diketik)
4. Tambah mahasiswa baru beserta nilai tugas, UTS, UAS (tersimpan ke JSON)
5. Hapus mahasiswa berdasarkan NIM (tersimpan ke JSON)
6. Rekapitulasi jumlah per kelas, jumlah lulus/tidak lulus, dan rata-rata nilai (tersimpan ke `output/rekap_mahasiswa.json`)
7. Ekspor seluruh data beserta nilai akhir, grade, dan status ke CSV (`output/mahasiswa.csv`)

## Teknologi dan Dependency
- Python 3.8+ (diuji dengan Python 3.13)
- Hanya standard library: `json`, `csv`, `logging`, `pathlib`
- Tidak ada library eksternal, tidak perlu `pip install`

## Struktur Folder
```
student_management/
├── main.py                      # menu CLI dan alur program
├── mahasiswa_app/               # package buatan sendiri
│   ├── __init__.py
│   ├── data_manager.py          # baca/simpan JSON
│   └── mahasiswa_service.py     # cari, filter, tambah, hapus, rekap
├── data/mahasiswa.json          # data utama (JSON)
├── output/rekap_mahasiswa.json  # hasil rekap (menu 6)
├── output/mahasiswa.csv         # hasil ekspor (menu 7)
└── README.md
```
Alur dependensi: `main.py` mengimpor dari package `mahasiswa_app`. `__init__.py` mengekspor function dari `mahasiswa_service.py` dan `data_manager.py`; kedua module tersebut tidak saling mengimpor.

Catatan: fungsi tambah dan hapus tidak mengubah list asli, tetapi mengembalikan list baru. Pesan log (INFO/WARNING/ERROR) tampil di terminal bersama output menu.

## Cara Menjalankan
Windows (PowerShell/CMD) atau Linux/macOS, dari dalam folder `student_management`:
```
cd student_management
python main.py        # Windows
python3 main.py       # Linux/macOS
```

## Aturan Data
- NIM dan kelas **bebas** (tidak harus berpola tertentu), tetapi tidak boleh kosong.
- NIM harus unik; spasi di awal/akhir NIM dihapus.
- Kelas disimpan dengan huruf besar (contoh: `ti-3a` menjadi `TI-3A`).
- Rekap per kelas dibuat otomatis dari kelas yang ada di data.

## Aturan Nilai
- Nilai akhir = tugas x 30% + UTS x 30% + UAS x 40%
- Grade: A (>= 85), B (>= 75), C (di atas 70), D (70 ke bawah)
- Status: **Lulus** jika nilai akhir di atas 70 (tepat 70 = Tidak Lulus), selain itu Tidak Lulus
- Nilai grade dan status tidak disimpan di JSON, tetapi dihitung dari tugas, UTS, UAS

## Contoh Penggunaan
```
Pilih menu (0-7): 1
No  NIM         Nama              Kelas  Tugas   UTS   UAS  Akhir  Grade Status
-------------------------------------------------------------------------------------
1   25.83.1847  Andi Pratama      TK01      80    75    85  80.50  B     Lulus
2   25.83.6203  Siti Rahma        TK02      90    85    88  87.70  A     Lulus
3   25.83.9351  Bima Saputra      TK01      60    55    65  60.50  D     Tidak Lulus
```

## Format File
Format yang dipakai: **JSON** untuk data utama dan rekap, **CSV** untuk hasil ekspor.

Input `data/mahasiswa.json`:
```json
[
  {"nim": "25.83.1847", "nama": "Andi Pratama", "kelas": "TK01", "tugas": 80, "uts": 75, "uas": 85}
]
```
Output `output/rekap_mahasiswa.json`:
```json
{
  "total_mahasiswa": 3,
  "jumlah_per_kelas": {"TK01": 2, "TK02": 1},
  "jumlah_lulus": 2,
  "jumlah_tidak_lulus": 1,
  "rata_rata_nilai_akhir": 76.23
}
```

Output CSV `output/mahasiswa.csv`:
```
nim,nama,kelas,tugas,uts,uas,nilai_akhir,grade,status
25.83.1847,Andi Pratama,TK01,80,75,85,80.5,B,Lulus
```
Kode dan dokumentasi dibuat dengan bantuan AI (Claude, Anthropic), kemudian dijalankan, diuji, dan dipahami oleh penulis.
