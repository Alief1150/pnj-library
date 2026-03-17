from django.db import models


class Buku(models.Model):
    JENIS_BUKU = [
        ('fiksi', 'Fiksi'),
        ('teknik', 'Teknik'),
        ('sains', 'Sains'),
        ('bisnis', 'Bisnis'),
        ('sejarah', 'Sejarah'),
        ('lainnya', 'Lainnya'),
    ]

    FORMAT_FILE = [
        ('pdf', 'PDF'),
        ('epub', 'EPUB'),
    ]

    judul = models.CharField(max_length=255)
    penulis = models.CharField(max_length=255)
    deskripsi = models.TextField(blank=True)
    jenis = models.CharField(max_length=20, choices=JENIS_BUKU, default='lainnya')
    tahun_terbit = models.PositiveIntegerField(blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    file_buku = models.FileField(upload_to='buku/', blank=True, null=True)
    format_file = models.CharField(max_length=10, choices=FORMAT_FILE, blank=True, null=True)
    stok = models.PositiveIntegerField(default=1)
    tanggal_ditambahkan = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Buku'
        verbose_name_plural = 'Buku'
        ordering = ['-tanggal_ditambahkan']

    def __str__(self):
        return self.judul
