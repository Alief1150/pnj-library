# Demo Cron Job OpenClaw: Import Buku Library → my_kisah

Panduan ini menjelaskan **cara membuat cron job yang benar** untuk:
- ambil file dari: `/run/media/alief/HOLMES/- Recovery File (2) -/Library/`
- sinkron ke: `/home/alief/Documents/VSC/Django-App/my_kisah/buku/`
- import ke database Django
- generate cover buku otomatis

---

## 1) Script yang dijalankan cron

Path script:

`/home/alief/Documents/VSC/Django-App/my_kisah/scripts/import_buku_library.sh`

Isi alur script:
1. `rsync` PDF/EPUB dari folder Library ke `/my_kisah/buku`
2. `python manage.py import_buku --source /my_kisah/buku`
3. `python manage.py generate_covers`

> Jadi cron cukup memanggil script ini, tidak perlu tulis command panjang berulang-ulang.

---

## 2) Cara buat cron via CLI (yang dipakai sekarang)

### A. Buat job baru

```bash
~/.local/bin/openclaw cron add \
  --name "Import Buku Library -> my_kisah" \
  --cron "0 2 * * *" \
  --tz "Asia/Jakarta" \
  --session main \
  --system-event "exec:/home/alief/Documents/VSC/Django-App/my_kisah/scripts/import_buku_library.sh" \
  --description "Sync ebook dari HOLMES Library ke /my_kisah/buku, import DB, lalu generate cover" \
  --announce \
  --best-effort-deliver
```

### B. Cek job

```bash
~/.local/bin/openclaw cron list
~/.local/bin/openclaw cron status
```

### C. Jalankan manual (tes)

```bash
~/.local/bin/openclaw cron run <JOB_ID>
```

### D. Lihat riwayat hasil run

```bash
~/.local/bin/openclaw cron runs --id <JOB_ID> --limit 10
```

---

## 3) Cara buat via UI OpenClaw (untuk demo dosen)

1. Buka dashboard OpenClaw (`openclaw dashboard` / localhost:18789)
2. Masuk menu **Cron / Scheduler**
3. Klik **Add Job / New Job**
4. Isi:
   - **Name**: `Import Buku Library -> my_kisah`
   - **Description**: `Sync ebook dari HOLMES Library ke /my_kisah/buku, import DB, lalu generate cover`
   - **Schedule (cron)**: `0 2 * * *`
   - **Timezone**: `Asia/Jakarta`
   - **Session Target**: `main`
   - **Payload Type**: `System Event`
   - **System Event Text**:
     `exec:/home/alief/Documents/VSC/Django-App/my_kisah/scripts/import_buku_library.sh`
   - **Delivery**: announce (optional), best-effort ON
5. Save
6. Klik **Run Now** untuk test
7. Cek tab **Runs/History**

---

## 4) Kenapa sebelumnya bisa jalan walau tanpa path?

Karena ada 2 mode payload:

1. **agentTurn** (`--message "..."`)
   - Agent menerima instruksi teks bebas.
   - Kalau instruksinya umum, hasil bisa tidak spesifik (contoh: hanya refresh index).

2. **systemEvent** (`--system-event "..."`)
   - Event eksplisit.
   - Untuk eksekusi shell dipakai format: `exec:/path/script.sh`.

Kasus sebelumnya: job dibuat dengan instruksi umum sehingga tidak memaksa source/target path yang kamu inginkan.

---

## 5) Catatan penting (biar tidak error)

- Untuk `exec:/...`, pakai **Session Target = main**.
- Job `isolated` umumnya mengharapkan `agentTurn` message, bukan `exec`.
- Pastikan storage eksternal HOLMES ter-mount saat jadwal cron berjalan.
- Jika notifikasi gagal kirim, gunakan `best-effort-deliver` agar job tetap sukses proses import.

---

## 6) Checklist demo cepat

- [ ] `openclaw cron list` tampil job aktif
- [ ] script path benar dan executable
- [ ] klik **Run Now** di UI
- [ ] cek file baru masuk ke `/my_kisah/buku`
- [ ] cek data masuk DB (halaman aplikasi)
- [ ] cek cover otomatis terbuat

---

Selesai. File ini bisa langsung dipakai sebagai bahan demo/presentasi.