"""Module untuk membaca dan menyimpan file JSON dan CSV."""

import csv
import json
import os

# Lokasi folder proyek (satu tingkat di atas folder mahasiswa_app)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_DATA = os.path.join(BASE_DIR, "data", "mahasiswa.json")
FILE_REKAP = os.path.join(BASE_DIR, "output", "rekap_mahasiswa.json")
FILE_CSV_EKSPOR = os.path.join(BASE_DIR, "output", "mahasiswa.csv")
KOLOM_CSV = ["nim", "nama", "kelas", "tugas", "uts", "uas"]


def baca_json(path_file):
    """Membaca file JSON.

    Parameter : path_file (str) - lokasi file JSON.
    Return    : isi file JSON (list/dict).
    Error     : FileNotFoundError jika file tidak ada,
                ValueError jika format JSON tidak valid.
    """
    try:
        with open(path_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Format JSON rusak di baris {error.lineno}: {error.msg}")


def simpan_json(path_file, data):
    """Menyimpan data ke file JSON (folder dibuat jika belum ada).

    Parameter : path_file (str), data (list/dict).
    Return    : True jika berhasil disimpan.
    """
    os.makedirs(os.path.dirname(path_file), exist_ok=True)
    with open(path_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    return True


def muat_data_mahasiswa(path_file=FILE_DATA):
    """Membaca data mahasiswa dan memeriksa struktur isinya.

    Parameter : path_file (str) - lokasi file data mahasiswa.
    Return    : list of dict, tiap dict berisi nim, nama, kelas, tugas, uts, uas.
    Error     : FileNotFoundError, ValueError (format/struktur salah).
    """
    data = baca_json(path_file)
    if not isinstance(data, list):
        raise ValueError("Isi file harus berupa list data mahasiswa.")
    for item in data:
        if not isinstance(item, dict) or not {"nim", "nama", "kelas", "tugas", "uts", "uas"} <= set(item):
            raise ValueError("Setiap data harus berupa dictionary dengan kunci nim, nama, kelas, tugas, uts, uas.")
    return data


def simpan_csv(path_file, baris, kolom):
    """Menyimpan list of dict ke file CSV.

    Parameter : path_file (str), baris (list of dict), kolom (list nama kolom).
    Return    : True jika berhasil disimpan.
    """
    os.makedirs(os.path.dirname(path_file), exist_ok=True)
    with open(path_file, "w", encoding="utf-8-sig", newline="") as file:
        penulis = csv.DictWriter(file, fieldnames=kolom)
        penulis.writeheader()
        penulis.writerows(baris)
    return True
