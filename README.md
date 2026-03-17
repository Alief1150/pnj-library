# PNJ Library (Django)

Web perpustakaan digital untuk koleksi buku PNJ (PDF/EPUB), dengan fitur:
- Login pengguna
- Lihat koleksi buku
- Detail buku
- Baca online (PDF)
- Download buku
- Import buku otomatis dari folder

Repository: https://github.com/Alief1150/pnj-library

---

## Status Proyek

Saat ini proyek masih **tahap development**.

---

## 1) Setup & Install

## A. Windows (PowerShell)

### Prasyarat
- Python 3.11+ (cek: `python --version`)
- Git

### Langkah
```powershell
git clone https://github.com/Alief1150/pnj-library.git
cd pnj-library

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install django pillow

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Buka: `http://127.0.0.1:8000`

> Catatan: file `db.sqlite3` tidak di-track, jadi wajib jalankan `migrate`.

---

## B. WSL (Ubuntu/Debian di Windows)

### Prasyarat
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git rsync
```

### Langkah
```bash
git clone https://github.com/Alief1150/pnj-library.git
cd pnj-library

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install django pillow

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Akses dari browser Windows: `http://localhost:8000`

---

## C. Linux Distributions (Arch, Ubuntu, Fedora, dll)

### Prasyarat umum
- Python 3
- pip
- venv
- git
- rsync

### Contoh install paket

**Arch/Manjaro:**
```bash
sudo pacman -S --needed python python-pip git rsync
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git rsync
```

**Fedora:**
```bash
sudo dnf install -y python3 python3-pip git rsync
```

### Langkah jalankan
```bash
git clone https://github.com/Alief1150/pnj-library.git
cd pnj-library

python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install django pillow

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 2) Cara Pakai Web

## URL penting
- Home: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/login/`
- Koleksi buku: `http://127.0.0.1:8000/koleksi/`
- Admin Django: `http://127.0.0.1:8000/admin/`

## Login
1. Buat user admin:
```bash
python manage.py createsuperuser
```
2. Login via `/login/` atau `/admin/`.

---

## 3) Menambahkan Directory Buku (Import ke Perpustakaan)

Project ini punya command:
```bash
python manage.py import_buku --source "/path/ke/folder-buku"
```

Contoh Linux/WSL:
```bash
python manage.py import_buku --source "/home/user/ebooks"
python manage.py generate_covers
```

Contoh Windows:
```powershell
python manage.py import_buku --source "D:\Ebooks"
python manage.py generate_covers
```

Format file yang didukung: **.pdf** dan **.epub**.

---

## 4) Setup Cron Job Import Otomatis

Ada script siap pakai:
- `scripts/import_buku_library.sh`

Script ini melakukan:
1. Sinkron file PDF/EPUB dari source folder ke folder `buku/`
2. Jalankan `python manage.py import_buku`
3. Jalankan `python manage.py generate_covers`
4. Simpan log di folder `logs/`

## A. Linux/WSL dengan crontab

1. Edit path di script sesuai mesin kamu (`APP_DIR`, `SRC_DIR`)
2. Jadikan executable:
```bash
chmod +x scripts/import_buku_library.sh
```
3. Tambah cron:
```bash
crontab -e
```
Contoh jalan tiap hari jam 02:00:
```cron
0 2 * * * /home/USER/path/pnj-library/scripts/import_buku_library.sh >> /home/USER/path/pnj-library/logs/cron.log 2>&1
```

## B. OpenClaw Cron (opsional)

Contoh:
```bash
openclaw cron add \
  --name "Import Buku Harian" \
  --cron "0 2 * * *" \
  --system-event "exec:/home/alief/Documents/VSC/Django-App/my_kisah/scripts/import_buku_library.sh" \
  --description "Import buku PNJ harian" \
  --tz "Asia/Jakarta"
```

---

## 5) Perintah Development Cepat

```bash
# cek konfigurasi
python manage.py check

# migrasi DB
python manage.py migrate

# jalankan server
python manage.py runserver

# import buku manual
python manage.py import_buku --source "/path/buku"

# generate cover
python manage.py generate_covers
```

---

## 6) Catatan Penting Repository

File/folder berikut tidak di-track Git (lihat `.gitignore`):
- `venv/`
- `media/`
- `buku/`
- `db.sqlite3`

Jadi setelah clone, kamu perlu setup environment + migrate dulu.

---

## License

Untuk kebutuhan pembelajaran/proyek internal.
