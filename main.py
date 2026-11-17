"""Program utama: menu CLI Sistem Pengelolaan Data Mahasiswa."""

import logging

from mahasiswa_app import (
    FILE_CSV,
    FILE_DATA,
    FILE_REKAP,
    KOLOM_CSV,
    buat_rekap,
    cari_mahasiswa,
    filter_kelas,
    hapus_mahasiswa,
    hitung_nilai_akhir,
    ke_angka,
    muat_data_mahasiswa,
    siapkan_baris_ekspor,
    simpan_csv,
    simpan_json,
    tambah_mahasiswa,
    tentukan_grade,
    tentukan_status,
    validasi_kelas,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("main")

def tampilkan_tabel(daftar):
    """Mencetak daftar mahasiswa beserta nilai, grade, dan status."""
    if not daftar:
        print("Data kosong.")
        return
    print(
        f"{'No':<4}{'NIM':<12}{'Nama':<18}{'Kls':<6}{'Tugas':>6}{'UTS':>6}"
        f"{'UAS':>6}{'Akhir':>7}  {'Grade':<6}{'Status'}"
    )
    print("-" * 85)
    for nomor, mhs in enumerate(daftar, start=1):
        akhir = hitung_nilai_akhir(mhs)
        print(
            f"{nomor:<4}{mhs['nim']:<12}{mhs['nama']:<18}{mhs['kelas']:<6}"
            f"{mhs['tugas']:>6g}{mhs['uts']:>6g}{mhs['uas']:>6g}{akhir:>7.2f}"
            f"  {tentukan_grade(akhir):<6}{tentukan_status(akhir)}"
        )

def tampilkan_menu():
    """Mencetak menu utama."""
    print("\n=== SISTEM PENGELOLAAN DATA MAHASISWA ===")
    print("1. Tampilkan semua data mahasiswa")
    print("2. Cari mahasiswa berdasarkan NIM")
    print("3. Filter mahasiswa berdasarkan kelas")
    print("4. Tambah mahasiswa baru")
    print("5. Hapus mahasiswa berdasarkan NIM")
    print("6. Rekapitulasi jumlah per kelas")
    print("7. Ekspor data ke CSV")
    print("0. Keluar")

def menu_cari(data):
    nim = input("Masukkan NIM: ").strip()
    mhs = cari_mahasiswa(data, nim)
    if mhs is None:
        logger.warning("NIM %s tidak ditemukan", nim)
        print(f"Data dengan NIM {nim} tidak ditemukan.")
        return
    tampilkan_tabel([mhs])

def menu_filter(data):
    kelas = input("Masukkan kelas (TK01/TK02): ").strip().upper()
    try:
        kelas = validasi_kelas(kelas)
    except ValueError as error:
        logger.warning("Filter ditolak: %s", error)
        print(error)
        return
    print(f"\nMahasiswa kelas {kelas}:")
    tampilkan_tabel(filter_kelas(data, kelas))

def menu_tambah(data):
    """Meminta data baru, lalu return list terbaru (data lama jika gagal)."""
    nim = input("NIM (25.83.XXXX): ").strip()
    nama = input("Nama: ").strip()
    kelas = input("Kelas (TK01/TK02): ").strip().upper()
    teks_tugas = input("Nilai tugas (0-100): ").strip()
    teks_uts = input("Nilai UTS (0-100): ").strip()
    teks_uas = input("Nilai UAS (0-100): ").strip()
    try:
        tugas = ke_angka(teks_tugas, "tugas")
        uts = ke_angka(teks_uts, "UTS")
        uas = ke_angka(teks_uas, "UAS")
        data_baru = tambah_mahasiswa(data, nim, nama, kelas, tugas, uts, uas)
        simpan_json(data_baru, FILE_DATA)
    except ValueError as error:
        logger.warning("Tambah data ditolak: %s", error)
        print(f"Gagal menambah data: {error}")
        return data
    except OSError as error:
        logger.error("Gagal menyimpan data: %s", error)
        print(f"Gagal mengakses file: {error}")
        return data
    else:
        mhs = data_baru[-1]
        print(f"Berhasil menambahkan {mhs['nama']} ({mhs['nim']}).")
        return data_baru

def menu_hapus(data):
    """Menghapus data berdasarkan NIM, lalu return list terbaru."""
    nim = input("NIM yang akan dihapus: ").strip()
    mhs = cari_mahasiswa(data, nim)
    try:
        data_baru = hapus_mahasiswa(data, nim)
        simpan_json(data_baru, FILE_DATA)
    except ValueError as error:
        logger.warning("Hapus data ditolak: %s", error)
        print(f"Gagal menghapus data: {error}")
        return data
    except OSError as error:
        logger.error("Gagal menyimpan data: %s", error)
        print(f"Gagal mengakses file: {error}")
        return data
    else:
        print(f"Data {mhs['nama']} ({mhs['nim']}) berhasil dihapus.")
        return data_baru

def menu_rekap(data):
    rekap = buat_rekap(data)
    print("\nREKAPITULASI MAHASISWA")
    for kelas, jumlah in rekap["jumlah_per_kelas"].items():
        print(f"  {kelas} : {jumlah} mahasiswa")
    print(f"  Total : {rekap['total_mahasiswa']} mahasiswa")
    print(
        f"  Lulus : {rekap['jumlah_lulus']} | "
        f"Tidak lulus : {rekap['jumlah_tidak_lulus']}"
    )
    print(f"  Rata-rata nilai akhir : {rekap['rata_rata_nilai_akhir']}")
    try:
        simpan_json(rekap, FILE_REKAP)
    except OSError as error:
        logger.error("Gagal menyimpan rekap: %s", error)
        print(f"Gagal mengakses file: {error}")
        return
    print("Rekap disimpan ke output/rekap_mahasiswa.json")

def menu_ekspor(data):
    baris = siapkan_baris_ekspor(data)
    kolom = KOLOM_CSV + ["nilai_akhir", "grade", "status"]
    try:
        simpan_csv(baris, FILE_CSV, kolom)
    except OSError as error:
        logger.error("Gagal membuat CSV: %s", error)
        print(f"Gagal mengakses file: {error}")
        return
    print(f"{len(baris)} data diekspor ke output/mahasiswa.csv")


def jalankan_menu(data):
    """Menampilkan menu berulang sampai pengguna memilih keluar."""
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (0-7): ").strip()
        if pilihan == "0":
            print("Terima kasih. Program selesai.")
            return
        elif pilihan == "1":
            tampilkan_tabel(data)
        elif pilihan == "2":
            menu_cari(data)
        elif pilihan == "3":
            menu_filter(data)
        elif pilihan == "4":
            data = menu_tambah(data)
        elif pilihan == "5":
            data = menu_hapus(data)
        elif pilihan == "6":
            menu_rekap(data)
        elif pilihan == "7":
            menu_ekspor(data)
        else:
            logger.warning("Pilihan menu tidak tersedia: %r", pilihan)
            print("Pilihan tidak valid. Masukkan angka 0-7.")

def main():
    """Memuat data lalu menjalankan menu."""
    try:
        data = muat_data_mahasiswa()
    except FileNotFoundError:
        logger.error("File data tidak ditemukan: %s", FILE_DATA)
        print(f"Error: file data tidak ditemukan di {FILE_DATA}")
        return
    except ValueError as error:
        logger.error("File data tidak valid: %s", error)
        print(f"Error: file data tidak bisa dibaca. {error}")
        return
    logger.info("%d data mahasiswa dimuat", len(data))
    try:
        jalankan_menu(data)
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan.")
    finally:
        logger.info("Sesi program selesai")

if __name__ == "__main__":
    main()