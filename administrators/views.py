from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from gis_data.models import Rumah
from .table import PP
from .forms import rumahForm, perumahanForm, kelurahanForm, kecamatanForm
from django.contrib import messages

# Create your views here.

@login_required(login_url='/login')
def index(request):

    isi = {
		'page_title': 'Utama',
    }
    return render(request,'administrators/index.html', isi)

@login_required(login_url='/login')
def pp(request):
    jumlah_rumah = Rumah.objects.count()
    jumlah_rlh = Rumah.objects.filter(status_rumah="RUMAH_LAYAK_HUNI").count()
    jumlah_rtlh = Rumah.objects.filter(status_rumah="RUMAH_TIDAK_LAYAK_HUNI").count()
    rawan_bencana = Rumah.objects.filter(rawan_bencana=True).count()
    isi = {
		'page_title': 'Perumahan & Permukiman',
    'subjudul': 'Perumahan & Permukiman',
    'jumlah_rumah': jumlah_rumah,
    'jumlah_rlh': jumlah_rlh,
    'jumlah_rtlh': jumlah_rtlh,
    'rawan_bencana': rawan_bencana,
    'icon_button': 'addhome',
    'button': 'Tambah Rumah',
    }
    return render(request,'administrators/pp.html', isi)


@login_required(login_url='/login')
def unitRumah(request):
    queryset = Rumah.objects.all()
    table = PP(queryset)

    isi = {
    'table': table,
		'page_title': 'Jumlah Unit Rumah',
    'subjudul': 'Jumlah Unit Rumah',
    'bc1' : 'bc1',
    'bc2' : 'bc2',
    # 'bc3' : 'bc3',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def RLH(request):   
    queryset = Rumah.objects.filter(status_rumah="RUMAH_LAYAK_HUNI")
    table = PP(queryset)

    isi = {
    'table': table,
		'page_title': 'Rumah Layak Huni',
    'subjudul': 'Rumah Layak Huni',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def RTLH(request):
    queryset = Rumah.objects.filter(status_rumah="RUMAH_TIDAK_LAYAK_HUNI")
    table = PP(queryset)

    isi = {
    'table': table,
		'page_title': 'Rumah Tidak Layak Huni',
    'subjudul': 'Rumah Tidak Layak Huni',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def rawanBencana(request):
    queryset = Rumah.objects.filter(rawan_bencana=True)
    table = PP(queryset)

    isi = {
    'table': table,
		'page_title': 'Rumah Dikawasan Bencana',
    'subjudul': 'Rumah Dikawasan Bencana',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def addRumah(request):
    post_form = rumahForm(request.POST or None)
    if request.method == 'POST':
      if post_form.is_valid():
        try:
          post_form.save()
          messages.success(request, 'Berhasil Menambahkan Data Rumah!')
          post_form = rumahForm()
        except Exception as e:
            messages.error(request, f'Gagal Untuk Menambahkan Data Rumah: {str(e)}')
      else:
          messages.error(request, 'Gagal Untuk Menambahkan Data Rumah. Periksa form untuk errors.')
    isi = {
		'page_title': 'Tambah Rumah',
    'subjudul': 'Tambah Rumah',
    'post_form': post_form,
    'button': 'Simpan',
    }
    return render(request,'administrators/forms.html', isi)

@login_required(login_url='/login')
def addPerumahan(request):
    post_form = perumahanForm(request.POST or None)
    
    if request.method == 'POST' and post_form.is_valid():
        try:
            perumahan = post_form.save()

            # Jika request dari popup Django Admin
            if "_popup" in request.GET:
                response_script = f"""
                <script>
                    opener.dismissAddAnotherPopup(window, "{perumahan.id_perumahan}", "{perumahan.nama_perumahan}");
                </script>
                """
                return HttpResponse(response_script)

            messages.success(request, 'Berhasil Menambahkan Data Perumahan!')
            post_form = perumahanForm()
        except Exception as e:
            messages.error(request, f'Gagal Untuk Menambahkan Data Perumahan: {str(e)}')

    isi = {
        'page_title': 'Tambah Perumahan',
        'subjudul': 'Tambah Perumahan',
        'post_form': post_form,
        'button': 'Simpan'
    }
    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login')
def addKelurahan(request):
    post_form = kelurahanForm(request.POST or None)
    
    if request.method == 'POST' and post_form.is_valid():
        try:
            kelurahan = post_form.save()

            # Jika request dari popup Django Admin
            if "_popup" in request.GET:
                response_script = f"""
                <script>
                    opener.dismissAddAnotherPopup(window, "{kelurahan.id_kelurahan}", "{kelurahan.kelurahan}");
                </script>
                """
                return HttpResponse(response_script)

            messages.success(request, 'Berhasil Menambahkan Data Kelurahan!')
            post_form = kelurahanForm()
        except Exception as e:
            messages.error(request, f'Gagal Untuk Menambahkan Data Kelurahan: {str(e)}')

    isi = {
        'page_title': 'Tambah Kelurahan',
        'subjudul': 'Tambah Kelurahan',
        'post_form': post_form,
        'button': 'Simpan'
    }
    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login')
def addKecamatan(request):
    post_form = kecamatanForm(request.POST or None)
    
    if request.method == 'POST' and post_form.is_valid():
        try:
            kecamatan = post_form.save()

            # Jika request dari popup Django Admin
            if "_popup" in request.GET:
                response_script = f"""
                <script>
                    opener.dismissAddAnotherPopup(window, "{kecamatan.id_kecamatan}", "{kecamatan.kecamatan}");
                </script>
                """
                return HttpResponse(response_script)

            messages.success(request, 'Berhasil Menambahkan Data Kecamatan!')
            post_form = kecamatanForm()
        except Exception as e:
            messages.error(request, f'Gagal Untuk Menambahkan Data Kecamatan: {str(e)}')

    isi = {
        'page_title': 'Tambah Kecamatan',
        'subjudul': 'Tambah Kecamatan',
        'post_form': post_form,
        'button': 'Simpan'
    }
    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login')
def activity_summary(request):

    isi = {
		'page_title': 'Aktivitas Pengguna',
    }
    return render(request,'administrators/table.html', isi)