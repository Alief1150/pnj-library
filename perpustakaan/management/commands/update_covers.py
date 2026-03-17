import os
import requests
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from perpustakaan.models import Buku


class Command(BaseCommand):
    help = 'Download cover images untuk buku yang belum ada cover'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Download ulang semua cover (termasuk yang sudah ada)',
        )

    def handle(self, *args, **kwargs):
        force = kwargs['force']

        # Filter buku yang perlu diupdate
        if force:
            buku_list = Buku.objects.all()
            self.stdout.write('Mode: Force update semua cover')
        else:
            buku_list = Buku.objects.filter(cover__isnull=True) | Buku.objects.filter(cover='')
            self.stdout.write('Mode: Hanya update buku tanpa cover')

        if not buku_list.exists():
            self.stdout.write(
                self.style.SUCCESS('Tidak ada buku yang perlu diupdate')
            )
            return

        self.stdout.write(f'Ditemukan {buku_list.count()} buku')

        success = 0
        failed = 0

        for buku in buku_list:
            try:
                # Generate cover URL
                cover_url = self.generate_cover_url(buku.judul)

                if not cover_url:
                    self.stdout.write(
                        self.style.WARNING(f'Skip: {buku.judul} - tidak bisa generate URL')
                    )
                    failed += 1
                    continue

                # Download cover
                response = requests.get(cover_url, timeout=10)
                if response.status_code == 200:
                    # Save to temporary file
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(response.content)
                    img_temp.flush()

                    # Save to model
                    img_filename = f"{self.sanitize_filename(buku.judul)}_cover.jpg"
                    buku.cover.save(img_filename, File(img_temp), save=True)

                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Download cover: {buku.judul}')
                    )
                    success += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Skip: {buku.judul} - HTTP {response.status_code}')
                    )
                    failed += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error: {buku.judul} - {str(e)}')
                )
                failed += 1

        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Download cover selesai!')
        self.stdout.write(f'  Sukses: {success} cover')
        self.stdout.write(f'  Gagal: {failed} cover')
        self.stdout.write('='*50)

    def generate_cover_url(self, judul):
        """Generate cover URL dari Google Books API"""
        try:
            # Clean judul for search
            search_query = judul.split('[')[0].split('(')[0].strip()
            search_query = ' '.join(search_query.split()[:5])  # Ambil 5 kata pertama

            # Gunakan Google Books API
            url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}&maxResults=1"

            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('totalCount', 0) > 0:
                    items = data.get('items', [])
                    if items and 'volumeInfo' in items[0]:
                        volume_info = items[0]['volumeInfo']
                        if 'imageLinks' in volume_info:
                            # Ambil thumbnail, ganti ke size lebih besar
                            thumbnail = volume_info['imageLinks'].get('thumbnail', '')
                            if thumbnail:
                                # Ganti http ke https dan ganti zoom level
                                return thumbnail.replace('http://', 'https://').replace('&zoom=1', '')

            # Fallback ke placeholder images
            return None

        except Exception:
            return None

    def sanitize_filename(self, filename):
        """Clean filename untuk penyimpanan"""
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:100]  # Limit length
