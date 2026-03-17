from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse
from django.conf import settings
import os
from .models import Buku


class CustomLoginView(LoginView):
    template_name = 'perpustakaan/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('koleksi_buku')


def home(request):
    # Ambil 6 buku terbaru untuk ditampilkan di halaman home
    buku_terbaru = Buku.objects.all()[:6]
    context = {
        'buku_terbaru': buku_terbaru,
    }
    return render(request, 'perpustakaan/home.html', context)


@login_required
def koleksi_buku(request):
    semua_buku = Buku.objects.all()
    context = {
        'semua_buku': semua_buku,
    }
    return render(request, 'perpustakaan/koleksi.html', context)


@login_required
def detail_buku(request, buku_id):
    buku = Buku.objects.get(id=buku_id)
    context = {
        'buku': buku,
    }
    return render(request, 'perpustakaan/detail.html', context)


@login_required
def baca_online(request, buku_id):
    """Baca PDF secara online di browser"""
    buku = Buku.objects.get(id=buku_id)

    if not buku.file_buku:
        return redirect('perpustakaan:detail_buku', buku_id=buku_id)

    if buku.format_file != 'pdf':
        return redirect('perpustakaan:baca_epub', buku_id=buku_id)

    # Serve PDF untuk dibaca di browser
    file_path = buku.file_buku.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else:
        return redirect('perpustakaan:detail_buku', buku_id=buku_id)


@login_required
def baca_epub(request, buku_id):
    """Buka EPUB di Okular"""
    buku = Buku.objects.get(id=buku_id)

    if not buku.file_buku:
        return redirect('perpustakaan:detail_buku', buku_id=buku_id)

    if buku.format_file != 'epub':
        return redirect('perpustakaan:baca_online', buku_id=buku_id)

    file_path = buku.file_buku.path

    # Buat HTML dengan JavaScript untuk membuka Okular
    context = {
        'buku': buku,
        'file_path': file_path,
    }
    return render(request, 'perpustakaan/baca_epub.html', context)


@login_required
def download_buku(request, buku_id):
    """Download file buku"""
    buku = Buku.objects.get(id=buku_id)

    if not buku.file_buku:
        return redirect('perpustakaan:detail_buku', buku_id=buku_id)

    file_path = buku.file_buku.path
    if os.path.exists(file_path):
        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(file_path)
        )
    else:
        return redirect('perpustakaan:detail_buku', buku_id=buku_id)
