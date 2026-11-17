"""Module untuk proses data mahasiswa: cari, filter, tambah, hapus, nilai, rekap."""

# Set dipakai karena pengecekan "apakah kelas valid" cepat dan tanpa duplikat
KELAS_VALID = {"TK01", "TK02"}


# Bobot nilai akhir (persen): tugas 30, UTS 30, UAS 40
BOBOT_TUGAS, BOBOT_UTS, BOBOT_UAS = 30, 30, 40
BATAS_LULUS = 70  # lulus jika nilai akhir DI ATAS 70


def ke_angka(teks, nama_nilai):
    """Mengubah teks input menjadi angka 0-100.

    Parameter : teks (str), nama_nilai (str) untuk pesan error.
    Return    : nilai (float).
    Error     : ValueError jika bukan angka atau di luar 0-100.
    """
    try:
        nilai = float(teks.replace(",", "."))
    except ValueError:
        raise ValueError(f"Nilai {nama_nilai} harus berupa angka.")
    if nilai < 0 or nilai > 100:
        raise ValueError(f"Nilai {nama_nilai} harus antara 0 sampai 100.")
    return int(nilai) if nilai == int(nilai) else nilai  # 85.0 -> 85


def hitung_nilai_akhir(mhs):
    """Menghitung nilai akhir berbobot. Return float (dibulatkan 2 desimal)."""
    total = (mhs["tugas"] * BOBOT_TUGAS + mhs["uts"] * BOBOT_UTS
             + mhs["uas"] * BOBOT_UAS) / 100
    return round(total, 2)


def tentukan_grade(nilai_akhir):
    """Menentukan grade: A (>=85), B (>=75), C (>70), selain itu D."""
    if nilai_akhir >= 85:
        return "A"
    elif nilai_akhir >= 75:
        return "B"
    elif nilai_akhir > BATAS_LULUS:
        return "C"
    else:
        return "D"


def tentukan_status(nilai_akhir):
    """Return 'Lulus' jika nilai akhir di atas 70, selain itu 'Tidak Lulus'."""
    return "Lulus" if nilai_akhir > BATAS_LULUS else "Tidak Lulus"


def validasi_nim(nim):
    """Cek format NIM 25.83.XXXX (XXXX = 4 angka). Return True/False."""
    return (len(nim) == 10
            and nim.startswith("25.83.")
            and all(c in "0123456789" for c in nim[6:]))


def cari_mahasiswa(data, nim):
    """Mencari mahasiswa berdasarkan NIM.

    Parameter : data (list of dict), nim (str).
    Return    : dictionary mahasiswa, atau None jika tidak ditemukan.
    """
    for mhs in data:
        if mhs["nim"] == nim:
            return mhs
    return None


def filter_kelas(data, kelas):
    """Mengambil mahasiswa pada satu kelas. Return list of dict."""
    return [mhs for mhs in data if mhs["kelas"] == kelas]  # list comprehension


def tambah_mahasiswa(data, nim, nama, kelas, tugas, uts, uas):
    """Menambah mahasiswa baru setelah semua input divalidasi.

    Parameter : data (list), nim, nama, kelas (str), tugas, uts, uas (angka 0-100).
    Return    : dictionary mahasiswa yang baru ditambahkan.
    Error     : ValueError dengan pesan yang jelas jika input tidak valid.
    """
    if not validasi_nim(nim):
        raise ValueError("Format NIM salah. Gunakan pola 25.83.XXXX (contoh: 25.83.1234).")
    nim_terdaftar = {mhs["nim"] for mhs in data}  # set comprehension
    if nim in nim_terdaftar:
        raise ValueError(f"NIM {nim} sudah terdaftar.")
    if nama == "":
        raise ValueError("Nama tidak boleh kosong.")
    if kelas not in KELAS_VALID:
        raise ValueError("Kelas tidak valid. Pilih TK01 atau TK02.")
    if not all(0 <= n <= 100 for n in (tugas, uts, uas)):
        raise ValueError("Nilai tugas, UTS, dan UAS harus antara 0 sampai 100.")
    mhs_baru = {"nim": nim, "nama": nama, "kelas": kelas,
                "tugas": tugas, "uts": uts, "uas": uas}
    data.append(mhs_baru)
    return mhs_baru


def hapus_mahasiswa(data, nim):
    """Menghapus mahasiswa berdasarkan NIM.

    Return : dictionary mahasiswa yang dihapus.
    Error  : ValueError jika NIM tidak ditemukan.
    """
    mhs = cari_mahasiswa(data, nim)
    if mhs is None:
        raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan.")
    data.remove(mhs)
    return mhs


def buat_rekap(data):
    """Membuat rekap jumlah per kelas, jumlah lulus/tidak lulus, dan rata-rata.

    Return : dictionary berisi total, jumlah_per_kelas, jumlah_lulus,
             jumlah_tidak_lulus, dan rata_rata_nilai_akhir.
    """
    jumlah = {kelas: len(filter_kelas(data, kelas))
              for kelas in sorted(KELAS_VALID)}  # dictionary comprehension
    nilai_akhir = [hitung_nilai_akhir(mhs) for mhs in data]
    lulus = len([n for n in nilai_akhir if n > BATAS_LULUS])
    rata_rata = round(sum(nilai_akhir) / len(nilai_akhir), 2) if nilai_akhir else 0
    return {"total_mahasiswa": len(data),
            "jumlah_per_kelas": jumlah,
            "jumlah_lulus": lulus,
            "jumlah_tidak_lulus": len(data) - lulus,
            "rata_rata_nilai_akhir": rata_rata}


def siapkan_baris_ekspor(data):
    """Menyiapkan data untuk CSV: setiap baris ditambah nilai akhir, grade, status.

    Return : list of dict.
    """
    baris = []
    for mhs in data:
        akhir = hitung_nilai_akhir(mhs)
        baris_baru = dict(mhs)
        baris_baru["nilai_akhir"] = akhir
        baris_baru["grade"] = tentukan_grade(akhir)
        baris_baru["status"] = tentukan_status(akhir)
        baris.append(baris_baru)
    return baris
