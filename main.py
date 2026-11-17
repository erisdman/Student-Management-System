"""Program utama: menu CLI Sistem Pengelolaan Data Mahasiswa."""

from mahasiswa_app import data_manager, mahasiswa_service


def tampilkan_tabel(daftar):
    """Mencetak daftar mahasiswa beserta nilai, grade, dan status."""
    if not daftar:
        print("Data kosong.")
        return
    print(f"{'No':<4}{'NIM':<12}{'Nama':<18}{'Kls':<6}{'Tugas':>6}{'UTS':>6}"
          f"{'UAS':>6}{'Akhir':>7}  {'Grade':<6}{'Status'}")
    print("-" * 85)
    for no, mhs in enumerate(daftar, start=1):
        akhir = mahasiswa_service.hitung_nilai_akhir(mhs)
        grade = mahasiswa_service.tentukan_grade(akhir)
        status = mahasiswa_service.tentukan_status(akhir)
        print(f"{no:<4}{mhs['nim']:<12}{mhs['nama']:<18}{mhs['kelas']:<6}"
              f"{mhs['tugas']:>6g}{mhs['uts']:>6g}{mhs['uas']:>6g}{akhir:>7.2f}"
              f"  {grade:<6}{status}")


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
    mhs = mahasiswa_service.cari_mahasiswa(data, nim)
    if mhs is None:
        print(f"Data dengan NIM {nim} tidak ditemukan.")
    else:
        tampilkan_tabel([mhs])


def menu_filter(data):
    kelas = input("Masukkan kelas (TK01/TK02): ").strip().upper()
    if kelas not in mahasiswa_service.KELAS_VALID:
        print("Kelas tidak valid. Pilih TK01 atau TK02.")
        return
    hasil = mahasiswa_service.filter_kelas(data, kelas)
    print(f"\nMahasiswa kelas {kelas}:")
    tampilkan_tabel(hasil)


def menu_tambah(data):
    nim = input("NIM: ").strip()
    nama = input("Nama: ").strip()
    kelas = input("Kelas (TK01/TK02): ").strip().upper()
    teks_tugas = input("Nilai tugas (0-100): ").strip()
    teks_uts = input("Nilai UTS (0-100): ").strip()
    teks_uas = input("Nilai UAS (0-100): ").strip()
    try:
        tugas = mahasiswa_service.ke_angka(teks_tugas, "tugas")
        uts = mahasiswa_service.ke_angka(teks_uts, "UTS")
        uas = mahasiswa_service.ke_angka(teks_uas, "UAS")
        mhs = mahasiswa_service.tambah_mahasiswa(data, nim, nama, kelas, tugas, uts, uas)
        data_manager.simpan_json(data_manager.FILE_DATA, data)
        print(f"Berhasil menambahkan {mhs['nama']} ({mhs['nim']}).")
    except ValueError as error:
        print(f"Gagal menambah data: {error}")


def menu_hapus(data):
    nim = input("NIM yang akan dihapus: ").strip()
    try:
        mhs = mahasiswa_service.hapus_mahasiswa(data, nim)
        data_manager.simpan_json(data_manager.FILE_DATA, data)
        print(f"Data {mhs['nama']} ({mhs['nim']}) berhasil dihapus.")
    except ValueError as error:
        print(f"Gagal menghapus data: {error}")


def menu_rekap(data):
    rekap = mahasiswa_service.buat_rekap(data)
    print("\nREKAPITULASI MAHASISWA")
    for kelas, jumlah in rekap["jumlah_per_kelas"].items():
        print(f"  {kelas} : {jumlah} mahasiswa")
    print(f"  Total : {rekap['total_mahasiswa']} mahasiswa")
    print(f"  Lulus : {rekap['jumlah_lulus']} | Tidak lulus : {rekap['jumlah_tidak_lulus']}")
    print(f"  Rata-rata nilai akhir : {rekap['rata_rata_nilai_akhir']}")
    data_manager.simpan_json(data_manager.FILE_REKAP, rekap)
    print("Rekap disimpan ke output/rekap_mahasiswa.json")


def menu_ekspor(data):
    baris = mahasiswa_service.siapkan_baris_ekspor(data)
    kolom = data_manager.KOLOM_CSV + ["nilai_akhir", "grade", "status"]
    data_manager.simpan_csv(data_manager.FILE_CSV_EKSPOR, baris, kolom)
    print(f"{len(baris)} data diekspor ke output/mahasiswa.csv")


def main():
    """Memuat data lalu menjalankan menu sampai pengguna memilih keluar."""
    try:
        data = data_manager.muat_data_mahasiswa()
    except FileNotFoundError:
        print(f"Error: file data tidak ditemukan di {data_manager.FILE_DATA}")
        return
    except ValueError as error:
        print(f"Error: file data tidak bisa dibaca. {error}")
        return

    aksi = {"2": menu_cari, "3": menu_filter, "4": menu_tambah,
            "5": menu_hapus, "6": menu_rekap, "7": menu_ekspor}

    while True:
        tampilkan_menu()
        try:
            pilihan = input("Pilih menu (0-7): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nProgram dihentikan.")
            break

        if pilihan == "0":
            print("Terima kasih. Program selesai.")
            break
        elif pilihan == "1":
            tampilkan_tabel(data)
        elif pilihan in aksi:
            try:
                aksi[pilihan](data)
            except (EOFError, KeyboardInterrupt):
                print("\nProgram dihentikan.")
                break
            except OSError as error:
                print(f"Gagal mengakses file: {error}")
        else:
            print("Pilihan tidak valid. Masukkan angka 0-7.")


if __name__ == "__main__":
    main()
