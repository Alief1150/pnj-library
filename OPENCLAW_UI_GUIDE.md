# Panduan Membuat Cron Job Lewat UI OpenClaw

## Cara Mengakses UI OpenClaw

### 1. Pastikan Gateway Berjalan

```bash
# Jalankan OpenClaw Gateway
~/.local/bin/openclaw gateway

# Atau jalankan di background
~/.local/bin/openclaw gateway --daemon
```

### 2. Buka UI Web Dashboard

```bash
# Buka dashboard
~/.local/bin/openclaw dashboard
```

Atau buka langsung di browser:
- Default URL: `http://localhost:18789`
- Dev mode: `http://localhost:19001`

## Membuat Cron Job Lewat UI

### Langkah 1: Buka Cron Scheduler

1. Di dashboard, cari menu **"Cron"** atau **"Scheduler"**
2. Klik untuk masuk ke halaman Cron Jobs

### Langkah 2: Create New Job

1. Klik tombol **"Add Job"** atau **"Create New"**
2. Isi form berikut:

#### Form Fields:

| Field | Deskripsi | Contoh |
|-------|-----------|--------|
| **Name** | Nama unik untuk cron job | `Import Buku PNJ` |
| **Description** | Deskripsi job | `Import buku otomatis dari folder buku/` |
| **Schedule** | Jadwal eksekusi | `0 2 * * *` (setiap jam 2 pagi) |
| **Interval** | Atau pakai interval | `6h` (setiap 6 jam) |
| **Message** | Pesan untuk agent | `Import buku dari folder` |
| **System Event** | Event sistem | `import_buku` |
| **Timezone** | Zona waktu | `Asia/Jakarta` |
| **Enabled** | Aktifkan job | ✅ Check |

### Langkah 3: Konfigurasi Schedule

Pilih salah satu metode scheduling:

#### Option A: Cron Expression
```
# Setiap hari jam 2 pagi
0 2 * * *

# Setiap 6 jam
0 */6 * * *

# Setiap minggu jam 00:00
0 0 * * 0

# Setiap tanggal 1 bulan
0 0 1 * *
```

#### Option B: Interval
```
6h    # Setiap 6 jam
30m   # Setiap 30 menit
1d    # Setiap hari
```

#### Option C: One-Time (At specific time)
```
2026-03-15T02:00:00  # 15 Maret 2026 jam 2 pagi
+10m                 # 10 menit dari sekarang
```

### Langkah 4: Save dan Test

1. Klik **"Save"** atau **"Create Job"**
2. Job akan muncul di list cron jobs
3. Klik tombol **"Run Now"** untuk test
4. Cek **"History"** atau **"Runs"** untuk melihat hasil

## Mengelola Cron Job di UI

### List Semua Jobs
- Di halaman Cron, semua job akan ter-list
- Dapat melihat status, next run, last run

### Enable/Disable Job
1. Cari job di list
2. Klik toggle switch atau tombol **"Enable/Disable"**

### Edit Job
1. Klik job yang ingin diedit
2. Klik **"Edit"** atau tombol pencil
3. Update field yang diinginkan
4. Klik **"Save"**

### Delete Job
1. Klik job yang ingin dihapus
2. Klik **"Delete"** atau tombol sampah
3. Konfirmasi delete

### View Run History
1. Klik job
2. Klik tab **"History"** atau **"Runs"**
3. Lihat log dari setiap eksekusi

## Contoh Cron Job untuk Import Buku

### Contoh 1: Import Harian

```
Name: Import Buku Harian
Description: Import buku otomatis setiap hari jam 2 pagi
Schedule: 0 2 * * *
Timezone: Asia/Jakarta
System Event: import_buku
Enabled: ✅
```

### Contoh 2: Import 6 Jam

```
Name: Import 6 Jam
Description: Import buku setiap 6 jam
Interval: 6h
System Event: import_buku
Enabled: ✅
```

### Contoh 3: One-Time Import

```
Name: Import Sekarang
Description: Import one-time sekarang
At: +0s
Delete After Run: ✅
System Event: import_buku
Enabled: ✅
```

## Cron Expression Builder (Jika Ada di UI)

Jika UI punya cron expression builder:

1. **Minute**: Pilih menit (0-59)
   - Contoh: `0` (di menit 0)

2. **Hour**: Pilih jam (0-23)
   - Contoh: `2` (jam 2 pagi)

3. **Day of Month**: Pilih tanggal (1-31)
   - Contoh: `*` (setiap tanggal)

4. **Month**: Pilih bulan (1-12)
   - Contoh: `*` (setiap bulan)

5. **Day of Week**: Pilih hari (0-6)
   - Contoh: `*` (setiap hari)

Hasil: `0 2 * * *`

## Monitoring Cron Jobs

### Real-time Status
- Cek status job (Active/Inactive)
- Next run time
- Last run status

### Notifications
- Configure email/webhook notifications
- Set alert untuk failed jobs
- Get summary setelah job selesai

## Troubleshooting via UI

### Job Tidak Jalan
1. Cek status job (enabled/disabled)
2. Cek next run time
3. Klik "Run Now" untuk test manual
4. Cek error log di tab "History"

### Gateway Tidak Connect
1. Cek status gateway di sidebar
2. Klik "Restart Gateway" jika perlu
3. Cek URL dan port

## Tips Menggunakan UI

1. **Gunakan Description yang Jelas**
   - Memudahkan tracking dan debugging

2. **Set Timezone yang Tepat**
   - Pastikan `Asia/Jakarta` untuk WIB

3. **Test Dulu dengan "Run Now"**
   - Pastikan job berjalan sebelum schedule

4. **Monitor History**
   - Cek apakah job berhasil atau gagal
   - Lihat log error jika ada

5. **Gunakan Interval untuk Sederhana**
   - Lebih mudah daripada cron expression

## Access dari Remote

### Enable Remote Access

```bash
# Edit config
~/.local/bin/openclaw config set gateway.remote.url https://your-domain.com
~/.local/bin/openclaw config set gateway.remote.token YOUR_TOKEN
```

Lalu akses UI dari remote browser.

## Keyboard Shortcuts (Jika Ada)

- `Ctrl/Cmd + N`: New Job
- `Ctrl/Cmd + E`: Edit Job
- `Ctrl/Cmd + D`: Delete Job
- `Ctrl/Cmd + R`: Run Now
- `Ctrl/Cmd + H`: History

## Mobile Access

UI OpenClaw biasanya responsive, bisa diakses dari:
- Smartphone browser
- Tablet browser
- Desktop browser

---

## Catatan untuk Import Buku PNJ

Script import sudah siap di:
- **Script**: `~/scripts/import_buku_pnj.sh`
- **Django Command**: `python manage.py import_buku`

Untuk menggunakan dengan OpenClaw cron:

1. Buka UI OpenClaw
2. Buat cron job baru
3. Set system event ke: `import_buku`
4. Atau gunakan message payload untuk custom commands

Happy scheduling! 🚀
