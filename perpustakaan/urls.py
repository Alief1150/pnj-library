from django.urls import path
from . import views

app_name = 'perpustakaan'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('koleksi/', views.koleksi_buku, name='koleksi_buku'),
    path('buku/<int:buku_id>/', views.detail_buku, name='detail_buku'),
    path('buku/<int:buku_id>/baca/', views.baca_online, name='baca_online'),
    path('buku/<int:buku_id>/epub/', views.baca_epub, name='baca_epub'),
    path('buku/<int:buku_id>/download/', views.download_buku, name='download_buku'),
]
