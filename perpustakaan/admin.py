from django.contrib import admin
from .models import Buku


@admin.register(Buku)
class BukuAdmin(admin.ModelAdmin):
    list_display = ('judul', 'penulis', 'jenis', 'format_file', 'tahun_terbit', 'stok', 'has_file')
    list_filter = ('jenis', 'format_file', 'tahun_terbit')
    search_fields = ('judul', 'penulis', 'deskripsi')
    list_per_page = 20
    readonly_fields = ('tanggal_ditambahkan',)

    def has_file(self, obj):
        return bool(obj.file_buku)
    has_file.boolean = True
    has_file.short_description = 'Ada File'
