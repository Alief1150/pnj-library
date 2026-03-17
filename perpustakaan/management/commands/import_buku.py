import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from perpustakaan.models import Buku


class Command(BaseCommand):
    help = 'Import buku dari direktori buku/ ke dalam database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='/home/alief/Documents/VSC/Django-App/my_kisah/buku/',
            help='Path ke direktori source buku',
        )
        parser.add_argument(
            '--delete-source',
            action='store_true',
            help='Hapus file source setelah import',
        )

    def handle(self, *args, **kwargs):
        source_dir = kwargs['source']
        delete_source = kwargs['delete_source']

        if not os.path.exists(source_dir):
            self.stdout.write(
                self.style.ERROR(f'Direktori {source_dir} tidak ditemukan')
            )
            return

        # Cari semua file PDF dan EPUB
        book_files = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.lower().endswith(('.pdf', '.epub')):
                    book_files.append(os.path.join(root, file))

        if not book_files:
            self.stdout.write(
                self.style.WARNING('Tidak ada file PDF atau EPUB ditemukan')
            )
            return

        self.stdout.write(f'Ditemukan {len(book_files)} file buku')

        imported = 0
        skipped = 0
        errors = 0

        for file_path in book_files:
            try:
                filename = os.path.basename(file_path)
                file_ext = filename.lower().split('.')[-1]

                # Ekstrak judul dari filename
                judul = self.extract_title(filename)

                # Cek apakah buku sudah ada
                if Buku.objects.filter(judul=judul).exists():
                    self.stdout.write(
                        self.style.WARNING(f'Skip: {judul} - sudah ada di database')
                    )
                    skipped += 1
                    continue

                # Tentukan jenis buku berdasarkan konten filename
                jenis = self.determine_jenis(filename, judul)

                # Tentukan penulis
                penulis = self.extract_author(filename)

                # Copy file ke media directory
                with open(file_path, 'rb') as f:
                    django_file = File(f)
                    buku = Buku(
                        judul=judul,
                        penulis=penulis,
                        jenis=jenis,
                        format_file=file_ext,
                        deskripsi=f'Buku {jenis} dengan format {file_ext.upper()}',
                        stok=999,  # Unlimited untuk e-book
                    )
                    buku.file_buku.save(f'buku/{filename}', django_file, save=True)

                self.stdout.write(
                    self.style.SUCCESS(f'✓ Import: {judul}')
                )
                imported += 1

                # Hapus file source jika diminta
                if delete_source:
                    os.remove(file_path)
                    self.stdout.write(f'  File source dihapus: {file_path}')

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error importing {file_path}: {str(e)}')
                )
                errors += 1

        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Import selesai!')
        self.stdout.write(f'  Berhasil: {imported} buku')
        self.stdout.write(f'  Skip: {skipped} buku')
        self.stdout.write(f'  Error: {errors} buku')
        self.stdout.write('='*50)

    def extract_title(self, filename):
        """Ekstrak judul dari filename"""
        # Hapus ekstensi file
        title = filename.rsplit('.', 1)[0]

        # Hapus nomor volume di awal (untuk light novel)
        title = title.strip()
        return title

    def determine_jenis(self, filename, judul):
        """Tentukan jenis buku berdasarkan filename"""
        filename_lower = filename.lower()
        judul_lower = judul.lower()

        # Cek kata kunci untuk setiap kategori
        if any(kw in filename_lower or kw in judul_lower for kw in [
            'cisco', 'ccna', 'mikrotik', 'mtcna', 'tcp', 'ip', 'network',
            'kotlin', 'python', 'java', 'programming', 'coding'
        ]):
            return 'teknik'
        elif any(kw in filename_lower or kw in judul_lower for kw in [
            'eighty six', '86 -', 'spice and wolf', 'novel', 'light novel'
        ]):
            return 'fiksi'
        elif any(kw in filename_lower or kw in judul_lower for kw in [
            'math', 'physics', 'chemistry', 'biology', 'science'
        ]):
            return 'sains'
        elif any(kw in filename_lower or kw in judul_lower for kw in [
            'business', 'management', 'economics', 'finance'
        ]):
            return 'bisnis'
        elif any(kw in filename_lower or kw in judul_lower for kw in [
            'history', 'sejarah', 'musashi'
        ]):
            return 'sejarah'

        return 'lainnya'

    def extract_author(self, filename):
        """Ekstrak nama penulis dari filename"""
        filename_lower = filename.lower()

        # Mapping known authors
        authors = {
            'muhammad_taufik': 'Muhammad Taufik',
            'aida_mahmudah': 'Aida Mahmudah',
            'asato': 'Asato Asato',
            'hasekura': 'Isuna Hasekura',
        }

        for key, value in authors.items():
            if key in filename_lower:
                return value

        # Default authors based on series
        if 'eighty six' in filename_lower or '86 -' in filename_lower:
            return 'Asato Asato'
        elif 'spice and wolf' in filename_lower:
            return 'Isuna Hasekura'
        elif 'musashi' in filename_lower:
            return 'Miyamoto Musashi'

        return 'Unknown Author'
