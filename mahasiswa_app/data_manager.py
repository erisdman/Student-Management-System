"""Membaca dan menyimpan data mahasiswa dalam format JSON dan CSV."""

import csv
import json
import logging
from pathlib import Path

logger = logging.getLogger("data_manager")

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_DATA = BASE_DIR / "data" / "mahasiswa.json"
FILE_REKAP = BASE_DIR / "output" / "rekap_mahasiswa.json"
FILE_CSV = BASE_DIR / "output" / "mahasiswa.csv"
KOLOM_CSV = ["nim", "nama", "kelas", "tugas", "uts", "uas"]
KOLOM_WAJIB = {"nim", "nama", "kelas", "tugas", "uts", "uas"}


def baca_json(path):
    """Membaca file JSON. Return isi file; ValueError jika JSON rusak."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Format JSON rusak di baris {error.lineno}: {error.msg}"
        )


def simpan_json(data, path):
    """Menyimpan data ke file JSON. Return True jika berhasil."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    logger.info("Data disimpan ke %s", path.name)
    return True


def muat_data_mahasiswa(path=FILE_DATA):
    """Membaca data mahasiswa dan memeriksa strukturnya. Return list of dict."""
    data = baca_json(path)
    if not isinstance(data, list):
        raise ValueError("Isi file harus berupa list data mahasiswa.")
    tidak_valid = any(
        not isinstance(item, dict) or not KOLOM_WAJIB <= set(item)
        for item in data
    )
    if tidak_valid:
        raise ValueError(
            "Setiap data harus berupa dictionary dengan kunci "
            "nim, nama, kelas, tugas, uts, uas."
        )
    return data


def simpan_csv(baris, path, kolom):
    """Menyimpan list of dict ke file CSV. Return True jika berhasil."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=kolom)
        writer.writeheader()
        writer.writerows(baris)
    logger.info("CSV dibuat: %s", path.name)
    return True
