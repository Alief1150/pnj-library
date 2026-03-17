import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from perpustakaan.models import Buku
from PIL import Image, ImageDraw, ImageFont
import io


class Command(BaseCommand):
    help = 'Generate placeholder cover images untuk buku'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Generate ulang semua cover (termasuk yang sudah ada)',
        )

    def handle(self, *args, **kwargs):
        force = kwargs['force']

        # Filter buku yang perlu diupdate
        if force:
            buku_list = Buku.objects.all()
            self.stdout.write('Mode: Force generate semua cover')
        else:
            buku_list = Buku.objects.filter(cover__isnull=True) | Buku.objects.filter(cover='')
            self.stdout.write('Mode: Hanya generate buku tanpa cover')

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
                # Generate cover
                cover_image = self.generate_cover(buku)

                # Save to temporary file
                img_temp = NamedTemporaryFile(delete=True, suffix='.png')
                cover_image.save(img_temp, 'PNG')
                img_temp.flush()

                # Save to model
                img_filename = f"{self.sanitize_filename(buku.judul)}_cover.png"
                buku.cover.save(img_filename, File(img_temp), save=True)

                self.stdout.write(
                    self.style.SUCCESS(f'✓ Generate cover: {buku.judul}')
                )
                success += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error: {buku.judul} - {str(e)}')
                )
                failed += 1

        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Generate cover selesai!')
        self.stdout.write(f'  Sukses: {success} cover')
        self.stdout.write(f'  Gagal: {failed} cover')
        self.stdout.write('='*50)

    def generate_cover(self, buku):
        """Generate cover image berdasarkan jenis buku"""
        # Warna berdasarkan jenis buku
        colors = {
            'fiksi': {'bg': '#fce4ec', 'accent': '#e91e63', 'text': '#880e4f'},
            'teknik': {'bg': '#e3f2fd', 'accent': '#2196f3', 'text': '#0d47a1'},
            'sains': {'bg': '#fff3e0', 'accent': '#ff9800', 'text': '#e65100'},
            'bisnis': {'bg': '#f3e5f5', 'accent': '#9c27b0', 'text': '#4a148c'},
            'sejarah': {'bg': '#efebe9', 'accent': '#795548', 'text': '#3e2723'},
            'lainnya': {'bg': '#e8f5e9', 'accent': '#4caf50', 'text': '#1b5e20'},
        }

        color_scheme = colors.get(buku.jenis, colors['lainnya'])

        # Create image
        width = 400
        height = 600
        img = Image.new('RGB', (width, height), color_scheme['bg'])
        draw = ImageDraw.Draw(img)

        # Try to use a custom font, fallback to default
        try:
            # Try common font paths
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
            ]
            title_font = None
            for path in font_paths:
                if os.path.exists(path):
                    title_font = ImageFont.truetype(path, 36)
                    break

            if not title_font:
                title_font = ImageFont.load_default()

            author_font = ImageFont.truetype(font_paths[0], 20) if title_font != ImageFont.load_default() else ImageFont.load_default()
            icon_font = ImageFont.truetype(font_paths[0], 80) if title_font != ImageFont.load_default() else ImageFont.load_default()

        except Exception:
            title_font = ImageFont.load_default()
            author_font = ImageFont.load_default()
            icon_font = ImageFont.load_default()

        # Icon berdasarkan format file
        icons = {
            'pdf': '📕',
            'epub': '📖',
            None: '📚'
        }
        icon_text = icons.get(buku.format_file, icons[None])

        # Draw icon
        try:
            # Get text bounding box
            icon_bbox = draw.textbbox((0, 0), icon_text, font=icon_font)
            icon_width = icon_bbox[2] - icon_bbox[0]
            icon_height = icon_bbox[3] - icon_bbox[1]
            icon_x = (width - icon_width) // 2
            icon_y = 80
            draw.text((icon_x, icon_y), icon_text, font=icon_font, fill=color_scheme['accent'])
        except Exception:
            # Fallback if emoji doesn't render
            pass

        # Draw title (multiline if needed)
        title = buku.judul
        words = title.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            if bbox[2] - bbox[0] < width - 60:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Limit to 3 lines
        lines = lines[:3]
        if len(buku.judul.split()) > 3 and len(lines) == 3:
            lines[-1] = lines[-1] + '...'

        # Draw title lines
        y_start = 200
        line_height = 45
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = y_start + (i * line_height)
            draw.text((x, y), line, font=title_font, fill=color_scheme['text'])

        # Draw author
        author = buku.penulis
        bbox = draw.textbbox((0, 0), author, font=author_font)
        author_width = bbox[2] - bbox[0]
        author_x = (width - author_width) // 2
        author_y = y_start + (len(lines) * line_height) + 20
        draw.text((author_x, author_y), author, font=author_font, fill=color_scheme['accent'])

        # Draw category badge
        category = buku.get_jenis_display()
        badge_y = height - 80
        badge_width = 200
        badge_height = 35
        badge_x = (width - badge_width) // 2

        # Draw rounded rectangle for badge
        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + badge_width, badge_y + badge_height],
            radius=10,
            fill=color_scheme['accent']
        )

        # Draw category text
        bbox = draw.textbbox((0, 0), category, font=author_font)
        cat_width = bbox[2] - bbox[0]
        cat_x = (width - cat_width) // 2
        cat_y = badge_y + 8
        draw.text((cat_x, cat_y), category, font=author_font, fill='white')

        # Draw format badge if available
        if buku.format_file:
            format_text = buku.get_format_file_display().upper()
            badge_y2 = badge_y - 45
            badge_width2 = 80
            badge_x2 = (width - badge_width2) // 2

            draw.rounded_rectangle(
                [badge_x2, badge_y2, badge_x2 + badge_width2, badge_y2 + badge_height],
                radius=10,
                fill=color_scheme['text']
            )

            bbox = draw.textbbox((0, 0), format_text, font=author_font)
            fmt_width = bbox[2] - bbox[0]
            fmt_x = (width - fmt_width) // 2
            fmt_y = badge_y2 + 8
            draw.text((fmt_x, fmt_y), format_text, font=author_font, fill='white')

        # Draw border
        draw.rectangle([10, 10, width-10, height-10], outline=color_scheme['accent'], width=4)

        return img

    def sanitize_filename(self, filename):
        """Clean filename untuk penyimpanan"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:100]
