# Prompt Instruksi Proyek Web Perpustakaan PNJ + Cron Job Backup

## Tujuan
Buat aplikasi web **Perpustakaan Politeknik Negeri Jakarta (PNJ)** dengan tampilan modern, akademik, profesional, dan dominan identitas kampus. Framework bebas mengikuti stack yang paling cocok untuk implementasi cepat dan rapi, tetapi prioritaskan struktur yang mudah dikembangkan dan mudah dipelihara.

---

## Konteks Umum
Bangun sistem web perpustakaan kampus yang memiliki:
- Landing page profil perpustakaan PNJ
- Halaman katalog buku
- Halaman login user
- Dashboard admin
- Dashboard user
- Sistem peminjaman sederhana
- Sistem pencatatan user login
- Sistem backup otomatis berbasis cron job

Aplikasi ditujukan untuk penggunaan **desktop-first**, tidak perlu fokus mobile secara penuh.

---

## Identitas Visual
Gunakan nuansa visual yang cocok untuk institusi akademik:
- Tema warna utama: biru tua / navy + emas / kuning lembut
- Gaya: modern, bersih, formal, profesional
- Hindari gaya terlalu playful
- UI harus terasa seperti sistem kampus resmi

---

## Fitur Utama Website

### 1. Landing Page
Buat landing page yang menampilkan:
- Hero section bertema perpustakaan PNJ
- Tentang perpustakaan
- Visi dan misi singkat
- Jam operasional
- Statistik singkat:
  - jumlah buku
  - jumlah kategori
  - jumlah member
- Call to action:
  - Lihat katalog
  - Login
- Footer berisi info institusi

### 2. Sistem User
Role minimal:
- Admin
- User / Mahasiswa

Fitur user:
- Login
- Logout
- Melihat katalog buku
- Mencari buku
- Filter buku berdasarkan kategori
- Melihat detail buku
- Riwayat login user tersimpan

### 3. Sistem Admin
Fitur admin:
- Dashboard statistik
- CRUD buku
- CRUD kategori
- CRUD user
- Melihat log user login
- Melihat daftar backup
- Melihat statistik jumlah buku dan user

### 4. Data Buku
Data buku minimal memiliki field:
- kode_buku
- judul
- penulis
- penerbit
- tahun_terbit
- kategori
- stok
- lokasi_rak
- deskripsi
- cover_buku (opsional)

### 5. Log Login User
Setiap user yang login harus tercatat:
- nama user
- email
- waktu login
- IP address
- user agent / device singkat

---

## Cron Job yang Wajib Dibuat

Buat 2 cron job utama:

### A. Backup Data Buku
Cron job ini harus:
- Mengambil seluruh data buku dari database
- Menyimpan hasil backup ke folder:
  `backup_routine/`
- Format file:
  `.md`
- Nama file:
  `backup_buku_YYYY-MM-DD.md`

Isi file backup buku harus memuat:
- tanggal backup
- total buku
- daftar buku lengkap dalam format tabel markdown
- ringkasan kategori jika memungkinkan

### B. Backup User Login
Cron job ini harus:
- Mengambil data log user yang login ke website
- Menyimpan hasil backup ke folder:
  `backup_routine/`
- Format file:
  `.md`
- Nama file:
  `backup_login_user_YYYY-MM-DD.md`

Isi file backup login harus memuat:
- tanggal backup
- total login tercatat
- daftar user login
- waktu login
- IP address
- device / browser singkat

---

## Scheduler / Implementasi Cron
Buat cron job berbasis scheduler framework dan sertakan juga perintah cron OS.

Jika menggunakan Laravel, gunakan:
- command artisan untuk backup buku
- command artisan untuk backup login user
- Laravel Scheduler untuk menjalankannya otomatis

Contoh schedule:
- Backup buku: setiap hari jam 01:00
- Backup login user: setiap hari jam 01:10

Contoh cron OS:
```cron
* * * * * cd /path/to/project && /usr/bin/php artisan schedule:run >> storage/logs/scheduler.log 2>&1
```

Jika menggunakan framework lain, sesuaikan tetapi tetap buat command/script backup yang jelas.

---

## Struktur Folder Backup
Pastikan sistem membuat folder berikut jika belum ada:
```bash
backup_routine/
```

File backup harus otomatis tersimpan di dalam folder tersebut.

---

## Database Minimal
Buat database dengan tabel minimal:

### users
- id
- name
- email
- password
- role
- created_at
- updated_at

### categories
- id
- nama_kategori
- created_at
- updated_at

### books
- id
- kode_buku
- judul
- penulis
- penerbit
- tahun_terbit
- category_id
- stok
- lokasi_rak
- deskripsi
- created_at
- updated_at

### login_logs
- id
- user_id
- ip_address
- user_agent
- login_at
- created_at
- updated_at

---

## Dashboard Admin
Dashboard admin harus menampilkan:
- total buku
- total kategori
- total user
- total login user
- tabel buku terbaru
- tabel login user terbaru

---

## Output yang Diminta
Tolong hasilkan:
1. Struktur project
2. Migration / schema database
3. Seeder dummy data
4. Halaman landing page
5. Dashboard admin
6. Dashboard user
7. Fitur CRUD buku
8. Sistem log login user
9. Command backup buku
10. Command backup login user
11. Scheduler / cron job
12. Penjelasan cara menjalankan project
13. Penjelasan cara mengaktifkan cron job

---

## Dummy Data
Tambahkan dummy data:
- beberapa kategori buku
- beberapa buku
- 1 akun admin
- 2 akun user mahasiswa
- beberapa log login user dummy

---

## Standar Implementasi
- Kode harus rapi
- Gunakan best practice framework
- Gunakan validasi form
- Gunakan layout admin yang konsisten
- Gunakan tabel yang bersih dan mudah dibaca
- Gunakan bahasa Indonesia pada UI

---

## Fokus Hasil
Tujuan utamanya adalah menghasilkan:
- website perpustakaan PNJ yang siap dikembangkan
- fitur backup otomatis yang benar-benar bisa dijalankan
- struktur proyek yang mudah dipahami mahasiswa

---

## Instruksi Tambahan untuk GLM / Claude Code
Tampilkan hasil dengan format:
- path file
- isi file
- command terminal
- langkah setup
- langkah menjalankan cron job

Jika memakai Laravel, sertakan:
- artisan command
- scheduler di console kernel / routes console sesuai versi Laravel
- lokasi folder backup
- isi contoh file markdown hasil backup

