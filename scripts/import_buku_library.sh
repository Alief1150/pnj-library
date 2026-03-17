#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/alief/Documents/VSC/Django-App/my_kisah"
SRC_DIR="/run/media/alief/HOLMES/- Recovery File (2) -/Library"
DST_DIR="$APP_DIR/buku"
LOG_DIR="$APP_DIR/logs"
TS="$(date +'%Y-%m-%d_%H-%M-%S')"
LOG_FILE="$LOG_DIR/import_buku_library_${TS}.log"

mkdir -p "$LOG_DIR" "$DST_DIR"

{
  echo "[$(date)] Start import buku library"
  echo "Source : $SRC_DIR"
  echo "Target : $DST_DIR"

  if [[ ! -d "$SRC_DIR" ]]; then
    echo "ERROR: source directory tidak ditemukan: $SRC_DIR"
    exit 1
  fi

  # Sinkron file ebook dari source ke folder buku app
  # --ignore-existing: tidak overwrite file lama
  rsync -av --ignore-existing \
    --include='*/' \
    --include='*.pdf' \
    --include='*.epub' \
    --exclude='*' \
    "$SRC_DIR/" "$DST_DIR/"

  cd "$APP_DIR"
  source "$APP_DIR/venv/bin/activate"

  # Import metadata ke database dari folder buku app
  python manage.py import_buku --source "$DST_DIR"

  # Generate cover untuk buku baru yang belum punya cover
  python manage.py generate_covers

  echo "[$(date)] Done import buku library"
} | tee "$LOG_FILE"
