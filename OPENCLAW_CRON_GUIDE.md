# Panduan Cron Job dengan OpenClaw

## Apa itu OpenClaw?

OpenClaw adalah CLI tool untuk mengelola cron jobs dan automation melalui Gateway WebSocket.

## Status Gateway

```bash
# Cek status gateway
~/.local/bin/openclaw status

# List semua cron jobs
~/.local/bin/openclaw cron list

# Cek status cron scheduler
~/.local/bin/openclaw cron status
```

## Struktur Perintah Cron

### Sintaks Dasar

```bash
openclaw cron add [options]
```

### Opsi Penting

| Opsi | Deskripsi | Contoh |
|------|-----------|--------|
| `--name <name>` | Nama cron job | `--name "Import Buku"` |
| `--cron <expr>` | Cron expression | `--cron "0 2 * * *"` |
| `--every <duration>` | Interval berulang | `--every "1h"`, `--every "30m"` |
| `--at <when>` | Run sekali pada waktu tertentu | `--at "2026-03-12T02:00:00"` |
| `--message <text>` | Pesan untuk agent | `--message "Import buku baru"` |
| `--system-event <text>` | Event sistem | `--system-event "import_books"` |
| `--description <text>` | Deskripsi job | `--description "Auto import buku dari folder buku/"` |
| `--disabled` | Buat job dalam keadaan disabled | `--disabled` |
| `--tz <iana>` | Timezone | `--tz "Asia/Jakarta"` |

## Contoh Penggunaan

### 1. Import Buku Setiap Hari Jam 2 Pagi

```bash
~/.local/bin/openclaw cron add \
  --name "Import Buku Harian" \
  --cron "0 2 * * *" \
  --system-event "import_buku" \
  --description "Import buku dari folder /home/alief/Documents/VSC/Django-App/my_kisah/buku/" \
  --tz "Asia/Jakarta"
```

### 2. Import Buku Setiap 6 Jam

```bash
~/.local/bin/openclaw cron add \
  --name "Import Buku 6 Jam" \
  --every "6h" \
  --system-event "import_buku" \
  --description "Auto import buku setiap 6 jam"
```

### 3. Import Buku Sekarang (One-shot)

```bash
~/.local/bin/openclaw cron add \
  --name "Import Buku Sekarang" \
  --at "+0s" \
  --system-event "import_buku" \
  --delete-after-run \
  --description "Import buku one-time"
```

### 4. Import Buku Pada Tanggal Tertentu

```bash
~/.local/bin/openclaw cron add \
  --name "Import Buku Scheduled" \
  --at "2026-03-15T02:00:00" \
  --system-event "import_buku" \
  --delete-after-run \
  --description "Import buku pada 15 Maret 2026 jam 2 pagi"
```

## Mengelola Cron Jobs

### List Semua Cron Jobs

```bash
~/.local/bin/openclaw cron list
```

### Disable Cron Job

```bash
~/.local/bin/openclaw cron disable --name "Import Buku Harian"
```

### Enable Cron Job

```bash
~/.local/bin/openclaw cron enable --name "Import Buku Harian"
```

### Hapus Cron Job

```bash
~/.local/bin/openclaw cron rm --name "Import Buku Harian"
```

### Edit Cron Job

```bash
~/.local/bin/openclaw cron edit --name "Import Buku Harian" --cron "0 3 * * *"
```

### Run Cron Job Sekarang (Debug)

```bash
~/.local/bin/openclaw cron run --name "Import Buku Harian"
```

### Lihat Riwayat Run

```bash
~/.local/bin/openclaw cron runs --name "Import Buku Harian"
```

## Cron Expression Format

OpenClaw menggunakan format cron 5-field atau 6-field (dengan seconds):

```
# Format 5-field (menit jam hari month weekday)
* * * * *
│ │ │ │ │
│ │ │ │ └─ Hari minggu (0-6, Minggu=0)
│ │ │ └─── Bulan (1-12)
│ │ └───── Hari tanggal (1-31)
│ └─────── Jam (0-23)
└───────── Menit (0-59)

# Format 6-field (detik menit jam hari month weekday)
* * * * * *
│ │ │ │ │ │
│ │ │ │ │ └─ Hari minggu (0-6, Minggu=0)
│ │ │ │ └─── Bulan (1-12)
│ │ │ └───── Hari tanggal (1-31)
│ │ └─────── Jam (0-23)
│ └───────── Menit (0-59)
└─────────── Detik (0-59)
```

### Contoh Cron Expression

| Expression | Deskripsi |
|------------|-----------|
| `0 2 * * *` | Setiap hari jam 2 pagi |
| `0 */6 * * *` | Setiap 6 jam |
| `0 0 * * 0` | Setiap minggu jam 00:00 |
| `0 0 1 * *` | Setiap tanggal 1 bulan |
| `*/30 * * * *` | Setiap 30 menit |
| `0 9-17 * * 1-5` | Jam 9-17, Senin-Jumat |

## Menggunakan TUI (Terminal UI)

Untuk pengalaman yang lebih interaktif:

```bash
# Buka TUI
~/.local/bin/openclaw tui

# Di dalam TUI, tekan:
# Ctrl+C -> Keluar
# ? -> Help
# / -> Search
```

## Script Import Buku

Untuk menggunakan OpenClaw cron dengan import buku, buat script terpisah:

### Buat Script: `~/scripts/import_buku.sh`

```bash
#!/bin/bash
cd /home/alief/Documents/VSC/Django-App/my_kisah
source venv/bin/activate
python manage.py import_buku
```

Jadikan executable:

```bash
chmod +x ~/scripts/import_buku.sh
```

### Update Cron dengan Script

```bash
~/.local/bin/openclaw cron add \
  --name "Import Buku Harian" \
  --cron "0 2 * * *" \
  --system-event "exec:/home/alief/scripts/import_buku.sh" \
  --description "Import buku setiap hari jam 2 pagi" \
  --tz "Asia/Jakarta"
```

## Troubleshooting

### Gateway Tidak Berjalan

```bash
# Jalankan gateway
~/.local/bin/openclaw gateway

# Atau di background
~/.local/bin/openclaw gateway --daemon
```

### Cek Log Cron Run

```bash
# Lihat riwayat run
~/.local/bin/openclaw cron runs --name "Nama Job"

# Format JSON
~/.local/bin/openclaw cron runs --name "Nama Job" --json
```

### Test Cron Job Sekarang

```bash
~/.local/bin/openclaw cron run --name "Nama Job"
```

## Tips

1. **Gunakan `--delete-after-run`** untuk one-shot jobs
2. **Gunakan `--disabled`** saat membuat job untuk testing dulu
3. **Set timezone** dengan `--tz "Asia/Jakarta"` untuk waktu Indonesia
4. **Use `--every`** untuk interval sederhana lebih mudah daripada cron expression
5. **Test dulu dengan `--run`** sebelum membiarkan cron berjalan otomatis

## Referensi

- OpenClaw Docs: https://docs.openclaw.ai/cli/cron
- Cron Expression Generator: https://crontab.guru/
