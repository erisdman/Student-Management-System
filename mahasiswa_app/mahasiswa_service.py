"""Logika data mahasiswa: validasi, pencarian, nilai, dan rekap."""

BOBOT = {"tugas": 30, "uts": 30, "uas": 40}
BATAS_LULUS = 70


class NamaKosongError(ValueError):
    """Nama mahasiswa belum diisi."""

def validasi_nim(nim):
    """Memeriksa NIM tidak kosong dan hanya berisi angka. Return NIM."""
    if not isinstance(nim, str) or not nim.strip():
        raise ValueError("NIM tidak boleh kosong.")
    nim = nim.strip()
    if not all(c in "0123456789" for c in nim):
        raise ValueError("NIM hanya boleh berisi angka.")
    return nim

def validasi_nama(value):
    """Memeriksa nama tidak kosong. Return nama tanpa spasi tepi."""
    if not isinstance(value, str) or not value.strip():
        raise NamaKosongError("Nama tidak boleh kosong.")
    return value.strip()


def validasi_kelas(value):
    """Memeriksa kelas tidak kosong. Return kelas huruf besar tanpa spasi tepi."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Kelas tidak boleh kosong.")
    return value.strip().upper()


def validasi_nilai(value, label):
    """Memeriksa nilai berupa angka 0-100. Return nilai."""
    if type(value) not in (int, float):
        raise ValueError(f"Nilai {label} harus berupa angka.")
    if not 0 <= value <= 100:
        raise ValueError(f"Nilai {label} harus antara 0 sampai 100.")
    return value


def ke_angka(teks, label):
    """Mengubah teks input menjadi angka 0-100. Return int atau float."""
    try:
        nilai = float(teks.replace(",", "."))
    except ValueError:
        raise ValueError(f"Nilai {label} harus berupa angka.")
    nilai = validasi_nilai(nilai, label)
    return int(nilai) if nilai == int(nilai) else nilai


def hitung_nilai_akhir(mhs):
    """Menghitung nilai akhir berbobot (2 desimal). Return float."""
    total = sum(mhs[nama] * bobot for nama, bobot in BOBOT.items()) / 100
    return round(total, 2)


def tentukan_grade(nilai_akhir):
    """Menentukan grade A, B, C, atau D. Return str."""
    if nilai_akhir >= 85:
        return "A"
    if nilai_akhir >= 75:
        return "B"
    if nilai_akhir > BATAS_LULUS:
        return "C"
    return "D"


def tentukan_status(nilai_akhir):
    """Menentukan status kelulusan. Return 'Lulus' atau 'Tidak Lulus'."""
    return "Lulus" if nilai_akhir > BATAS_LULUS else "Tidak Lulus"


def cari_mahasiswa(data, nim):
    """Mencari mahasiswa berdasarkan NIM. Return dictionary atau None."""
    nim = nim.strip()
    for mhs in data:
        if mhs["nim"] == nim:
            return mhs
    return None


def filter_kelas(data, kelas):
    """Mengambil mahasiswa satu kelas. Return list of dict."""
    return [mhs for mhs in data if mhs["kelas"] == kelas]


def tambah_mahasiswa(data, nim, nama, kelas, tugas, uts, uas):
    """Menambah mahasiswa baru tanpa mengubah data asli.

    Return list baru; ValueError jika ada input yang tidak valid.
    """
    nim = validasi_nim(nim)
    nim_terdaftar = {mhs["nim"] for mhs in data}
    if nim in nim_terdaftar:
        raise ValueError(f"NIM {nim} sudah terdaftar.")
    mhs_baru = {
        "nim": nim,
        "nama": validasi_nama(nama),
        "kelas": validasi_kelas(kelas),
        "tugas": validasi_nilai(tugas, "tugas"),
        "uts": validasi_nilai(uts, "UTS"),
        "uas": validasi_nilai(uas, "UAS"),
    }
    return [*data, mhs_baru]


def hapus_mahasiswa(data, nim):
    """Menghapus mahasiswa berdasarkan NIM tanpa mengubah data asli.

    Return list baru; ValueError jika NIM tidak ditemukan.
    """
    if cari_mahasiswa(data, nim) is None:
        raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan.")
    return [mhs for mhs in data if mhs["nim"] != nim]


def buat_rekap(data):
    """Membuat rekap jumlah per kelas, lulus/tidak lulus, dan rata-rata."""
    daftar_kelas = {mhs["kelas"] for mhs in data}
    jumlah = {
        kelas: len(filter_kelas(data, kelas))
        for kelas in sorted(daftar_kelas)
    }
    nilai_akhir = [hitung_nilai_akhir(mhs) for mhs in data]
    lulus = len([nilai for nilai in nilai_akhir if nilai > BATAS_LULUS])
    rata_rata = round(sum(nilai_akhir) / len(nilai_akhir), 2) if nilai_akhir else 0
    return {
        "total_mahasiswa": len(data),
        "jumlah_per_kelas": jumlah,
        "jumlah_lulus": lulus,
        "jumlah_tidak_lulus": len(data) - lulus,
        "rata_rata_nilai_akhir": rata_rata,
    }


def siapkan_baris_ekspor(data):
    """Menambah nilai akhir, grade, dan status pada tiap data untuk CSV."""
    baris = []
    for mhs in data:
        akhir = hitung_nilai_akhir(mhs)
        baris.append({
            **mhs,
            "nilai_akhir": akhir,
            "grade": tentukan_grade(akhir),
            "status": tentukan_status(akhir),
        })
    return baris
