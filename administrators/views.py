from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gis_data.models import Rumah, AddRequest, UpdateRequest
from django.db.models import Q

# Create your views here.

@login_required(login_url='/login')
def index(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()
    data_rumah_belum_lengkap = Rumah.objects.filter(
        Q(nama_perumahan__isnull=True) |
        Q(nama_pemilik__isnull=True) |
        Q(status_rumah__isnull=True) |
        Q(photo_rumah__isnull=True) |
        Q(alamat_rumah__isnull=True) |
        Q(jumlah_kk__isnull=True) |
        Q(nilai_kesehatan__isnull=True) |
        Q(nilai_keselamatan__isnull=True) |
        Q(nilai_komponen__isnull=True) |
        Q(status_luas__isnull=True) |
        Q(rumah_sewa__isnull=True) |
        Q(dibuat_oleh_users__isnull=True)
    ).count()
    total_pengajuan_belum_diproses = (
        AddRequest.objects.filter(disetujui=False, ditolak=False).count() +
        UpdateRequest.objects.filter(disetujui=False, ditolak=False).count()
    )
    total_pengajuan_saya_belum_diproses = (
        AddRequest.objects.filter(disetujui=False, ditolak=False, dibuat_oleh=request.user).count() +
        UpdateRequest.objects.filter(disetujui=False, ditolak=False, dibuat_oleh=request.user).count()
    )
    isi = {
		'page_title': 'Utama',
    'admin': admin,
    'operator': operator,
    'data_rumah_belum_lengkap': data_rumah_belum_lengkap,
    'total_pengajuan_belum_diproses': total_pengajuan_belum_diproses,
    'total_pengajuan_saya_belum_diproses': total_pengajuan_saya_belum_diproses,
    }
    return render(request,'administrators/index.html', isi)

