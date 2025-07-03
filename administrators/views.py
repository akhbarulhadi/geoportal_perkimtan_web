from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from gis_data.models import Rumah, Perumahan, RumahSusun, AddRequest, UpdateRequest
from .table import RumahTable, PerumahanTable, RusunTable, GeoDatasetTable, AddRequestRumahTable, UpdateRequestRumahTable
from .forms import rumahForm, perumahanForm, kelurahanForm, kecamatanForm, rusunForm, geoForm, RumahAddRequestForm
from django.contrib import messages
from django_tables2 import RequestConfig
from maps.models import GeoDataset
from django.db.models import Prefetch
from django.db.models import Q
from .logger import log_action
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import DELETION, ADDITION, CHANGE
from django.contrib.gis.geos import GEOSGeometry

# Create your views here.

@login_required(login_url='/login')
def index(request):

    isi = {
		'page_title': 'Utama',
    }
    return render(request,'administrators/index.html', isi)

@login_required(login_url='/login')
def activity(request):
    recent_actions = LogEntry.objects.filter(user=request.user).select_related('user', 'content_type').order_by('-action_time')[:20]

    isi = {
		'page_title': 'Aktivitas Pengguna',
		'subjudul': 'Aktivitas Pengguna',
        'recent_actions': recent_actions,
    }
    return render(request,'administrators/activity.html', isi)

@login_required(login_url='/login')
def pp(request):
    jumlah_rumah = GeoDataset.objects.filter(kategori="Unit Rumah").count()
    jumlah_rlh = Rumah.objects.filter(status_rumah="RUMAH_LAYAK_HUNI").count()
    jumlah_rtlh = Rumah.objects.filter(status_rumah="RUMAH_TIDAK_LAYAK_HUNI").count()
    jumlah_sewa = Rumah.objects.filter(rumah_sewa=True).count()
    rumah_subsidi = Rumah.objects.filter(nama_perumahan__perumahan_subsidi=True).count()

    perumahan = Perumahan.objects.count()
    perumahan_subsidi = Perumahan.objects.filter(perumahan_subsidi=True).count()

    rusun = RumahSusun.objects.count()

    isi = {
	'page_title': 'Permukiman',
    'subjudul': 'Permukiman',
    'jumlah_rumah': jumlah_rumah,
    'jumlah_rlh': jumlah_rlh,
    'jumlah_rtlh': jumlah_rtlh,
    'jumlah_sewa': jumlah_sewa,
    'rumah_subsidi': rumah_subsidi,
    'rusun': rusun,
    'perumahan': perumahan,
    'perumahan_subsidi': perumahan_subsidi,
    'icon_button': 'addhome',
    'button': 'Tambah Rumah',
    }
    return render(request,'administrators/pp.html', isi)


@login_required(login_url='/login')
def unitRumah(request):
    search_query = request.GET.get('search', '')
    
    queryset = GeoDataset.objects.select_related('rumah').filter(kategori='Unit Rumah').order_by('rumah__nama_pemilik')

    if search_query:
        queryset = queryset.filter(
            Q(rumah__nama_pemilik__icontains=search_query) |
            Q(rumah__id_rumah__icontains=search_query)
        )

    table = GeoDatasetTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Pemilik...'
    isi = {
        'placeholder_search' : placeholder_search,
        'table': table,
        'page_title': 'Jumlah Unit Rumah',
        'subjudul': 'Jumlah Unit Rumah',
    }
    return render(request, 'administrators/table_view.html', isi)


@login_required(login_url='/login')
def RLH(request):   
    search_query = request.GET.get('search', '')
    
    queryset = GeoDataset.objects.select_related('rumah') \
        .filter(kategori='Unit Rumah', rumah__status_rumah='RUMAH_LAYAK_HUNI') \
        .order_by('rumah__nama_pemilik')

    if search_query:
        queryset = queryset.filter(
            Q(rumah__nama_pemilik__icontains=search_query)
        )

    table = GeoDatasetTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Pemilik...'

    isi = {
    'placeholder_search' : placeholder_search,
    'table': table,
	'page_title': 'Rumah Layak Huni',
    'subjudul': 'Rumah Layak Huni',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def RTLH(request):
    search_query = request.GET.get('search', '')
    
    queryset = GeoDataset.objects.select_related('rumah') \
        .filter(kategori='Unit Rumah', rumah__status_rumah='RUMAH_TIDAK_LAYAK_HUNI') \
        .order_by('rumah__nama_pemilik')

    if search_query:
        queryset = queryset.filter(
            Q(rumah__nama_pemilik__icontains=search_query)
        )

    table = GeoDatasetTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Pemilik...'

    isi = {
    'placeholder_search' : placeholder_search,
    'table': table,
	'page_title': 'Rumah Tidak Layak Huni',
    'subjudul': 'Rumah Tidak Layak Huni',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def rumahSewa(request):
    search_query = request.GET.get('search', '')
    
    queryset = GeoDataset.objects.select_related('rumah') \
        .filter(kategori='Unit Rumah', rumah__rumah_sewa=True) \
        .order_by('rumah__nama_pemilik')

    if search_query:
        queryset = queryset.filter(
            Q(rumah__nama_pemilik__icontains=search_query)
        )

    table = GeoDatasetTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Pemilik...'

    isi = {
    'placeholder_search' : placeholder_search,
    'table': table,
	'page_title': 'Rumah Sewa',
    'subjudul': 'Rumah Sewa',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def perumahan(request):
    search_query = request.GET.get('search', '')
    queryset = Perumahan.objects.all()

    if search_query:
        queryset = queryset.filter(
            Q(nama_perumahan__icontains=search_query)
        )

    table = PerumahanTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Perumahan...'

    isi = {
    'placeholder_search' : placeholder_search,
    'table': table,
	'page_title': 'Perumahan',
    'subjudul': 'Perumahan',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def perumahanSubsidi(request):
    search_query = request.GET.get('search', '')
    queryset = Perumahan.objects.filter(perumahan_subsidi=True)

    if search_query:
        queryset = queryset.filter(
            Q(nama_perumahan__icontains=search_query)
        )

    table = PerumahanTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Perumahan...'

    isi = {
    'placeholder_search' : placeholder_search,
    'table': table,
	'page_title': 'Perumahan Subsidi',
    'subjudul': 'Perumahan Subsidi',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def rumahSubsidi(request):
    search_query = request.GET.get('search', '')

    queryset = GeoDataset.objects.select_related('rumah', 'rumah__nama_perumahan') \
        .filter(kategori='Unit Rumah', rumah__nama_perumahan__perumahan_subsidi=True) \
        .order_by('rumah__nama_pemilik')
    
    if search_query:
        queryset = queryset.filter(
            Q(rumah__nama_pemilik__icontains=search_query)
        )

    table = GeoDatasetTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Pemilik...'
    
    isi = {
    'placeholder_search' : placeholder_search,
    'table': table,
	'page_title': 'Rumah Subsidi',
    'subjudul': 'Rumah Subsidi',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def rumahSusun(request):
    search_query = request.GET.get('search', '')
    queryset = RumahSusun.objects.all()

    if search_query:
        queryset = queryset.filter(
            Q(nama_rusun__icontains=search_query)
        )

    table = RusunTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Rusun...'

    isi = {
    'placeholder_search' : placeholder_search,
    'table': table,
	'page_title': 'Rumah Susun',
    'subjudul': 'Rumah Susun',
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def addRumah(request):
    if request.method == 'POST':
        geo_form = geoForm(request.POST, request.FILES)
        rumah_form = rumahForm(request.POST, request.FILES)

        if geo_form.is_valid() and rumah_form.is_valid():
            try:
                geo_obj = geo_form.save(commit=False)
                geo_obj.nama_dataset = "Rumah Baru"
                geo_obj.kategori = "Unit Rumah"
                geo_obj.properties = {"sumber": "form"}

                geo_obj.save()

                rumah_obj = rumah_form.save(commit=False)
                rumah_obj.geo = geo_obj
                rumah_obj.save()

                log_action(request, geo_obj, ADDITION, f'Menambahkan Data: {geo_obj}')

                messages.success(request, 'Berhasil Menambahkan Data Rumah!')
                geo_form = geoForm()
                rumah_form = rumahForm()

            except Exception as e:
                messages.error(request, f'Gagal Untuk Menambahkan Data Rumah: {str(e)}')
        else:
            print("GeoForm Errors:", geo_form.errors)
            print("RumahForm Errors:", rumah_form.errors)
            messages.error(request, 'Gagal Untuk Menambahkan Data Rumah. Periksa form untuk errors.')
    else:
        geo_form = geoForm()
        rumah_form = rumahForm()

    isi = {
        'geo_form': geo_form,
        'post_form': rumah_form,
        'button': 'Simpan',
        'page_title': 'Tambah Rumah',
        'subjudul': 'Tambah Rumah',
    }
    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login')
def addPerumahan(request):    
    if request.method == 'POST':
        post_form = perumahanForm(request.POST, request.FILES)
        if post_form.is_valid():
            try:
                perumahan_obj = post_form.save()
                log_action(request, perumahan_obj, ADDITION, f'Menambahkan Data: {perumahan_obj}')
                messages.success(request, 'Berhasil Menambahkan Data Perumahan!')
                post_form = perumahanForm()
            except Exception as e:
                messages.error(request, f'Gagal Untuk Menambahkan Data Perumahan: {str(e)}')
    else:
        post_form = perumahanForm()

    isi = {
        'page_title': 'Tambah Perumahan',
        'subjudul': 'Tambah Perumahan',
        'post_form': post_form,
        'button': 'Simpan'
    }
    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login')
def addPerumahanPopUp(request):
    post_form = perumahanForm(request.POST or None)
    
    if request.method == 'POST' and post_form.is_valid():
        try:
            perumahan = post_form.save()

            # Jika request dari popup Django Admin
            if "_popup" in request.GET:
                log_action(request, perumahan, ADDITION, f'Menambahkan Data: {perumahan}')
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
    return render(request, 'administrators/forms_popup.html', isi)

@login_required(login_url='/login')
def addKelurahan(request):
    post_form = kelurahanForm(request.POST or None)
    
    if request.method == 'POST' and post_form.is_valid():
        try:
            kelurahan = post_form.save()

            # Jika request dari popup Django Admin
            if "_popup" in request.GET:
                log_action(request, kelurahan, ADDITION, f'Menambahkan Data: {kelurahan}')
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
    return render(request, 'administrators/forms_popup.html', isi)

@login_required(login_url='/login')
def addKecamatan(request):
    post_form = kecamatanForm(request.POST or None)
    
    if request.method == 'POST' and post_form.is_valid():
        try:
            kecamatan = post_form.save()

            # Jika request dari popup Django Admin
            if "_popup" in request.GET:
                log_action(request, kecamatan, ADDITION, f'Menambahkan Data: {kecamatan}')
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
    return render(request, 'administrators/forms_popup.html', isi)

@login_required(login_url='/login')
def addRusun(request):
    post_form = rusunForm(request.POST, request.FILES)
    
    if request.method == 'POST' and post_form.is_valid():
        try:
            rusun_obj = post_form.save()
            log_action(request, rusun_obj, ADDITION, f'Menambahkan Data: {rusun_obj}')
            messages.success(request, 'Berhasil Menambahkan Data Rumah Susun!')
            post_form = rusunForm()
        except Exception as e:
            messages.error(request, f'Gagal Untuk Menambahkan Data Rumah Susun: {str(e)}')

    isi = {
        'page_title': 'Tambah Rumah Susun',
        'subjudul': 'Tambah Rumah Susun',
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

@login_required(login_url='/') 
def updateRumah(request, pk): 
    geo_instance = get_object_or_404(GeoDataset, pk=pk)

    try:
        rumah_instance = geo_instance.rumah
    except Rumah.DoesNotExist:
        rumah_instance = Rumah(geo=geo_instance)

    if request.method == 'POST':
        geo_form = geoForm(request.POST, request.FILES, instance=geo_instance)
        rumah_form = rumahForm(request.POST, request.FILES, instance=rumah_instance)
        if geo_form.is_valid() and rumah_form.is_valid():
            try:
                geo_form.save()
                rumah_form.save()
                log_action(request, geo_instance, CHANGE, f'Mengubah Data: {geo_instance}')
                messages.success(request, 'Data berhasil berubah!')
                return redirect('administrators:update-rumah', pk=pk)
            except Exception as e:
                messages.error(request, f'Gagal merubah Data: {str(e)}')
        else:
            messages.error(request, 'Gagal merubah Data. Periksa form untuk errors.')
    else:
        geo_form = geoForm(instance=geo_instance)
        rumah_form = rumahForm(instance=rumah_instance)

    isi = {
        'page_title': 'Detail Data Rumah',
        'subjudul': 'Detail Data Rumah',
        'post_form': rumah_form,
        'geo_form': geo_form,
        'button': 'Edit',
    }

    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/') 
def updatePerumahan(request, pk): 
    update = get_object_or_404(Perumahan, pk=pk)

    if request.method == 'POST':
        update_form = perumahanForm(request.POST, request.FILES, instance=update)
        if update_form.is_valid():
            try:
                update_form.save()
                log_action(request, update, CHANGE, f'Mengubah Data: {update}')
                messages.success(request, 'Data berhasil berubah!')
                return redirect('administrators:update-perumahan', pk=pk)
            except Exception as e:
                messages.error(request, f'Gagal merubah Data: {str(e)}')
        else:
            messages.error(request, 'Gagal merubah Data. Periksa form untuk errors.')
    else:
        update_form = perumahanForm(instance=update)

    isi = {
        'page_title': 'Detail Data Perumahan',
        'subjudul': 'Detail Data Perumahan',
        'post_form': update_form,
        'button': 'Edit',
    }

    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/') 
def updateRusun(request, pk): 
    update = get_object_or_404(RumahSusun, pk=pk)

    if request.method == 'POST':
        update_form = rusunForm(request.POST, request.FILES, instance=update)
        if update_form.is_valid():
            try:
                update_form.save()
                log_action(request, update, CHANGE, f'Mengubah Data: {update}')
                messages.success(request, 'Data berhasil berubah!')
                return redirect('administrators:update-rusun', pk=pk)
            except Exception as e:
                messages.error(request, f'Gagal merubah Data: {str(e)}')
        else:
            messages.error(request, 'Gagal merubah Data. Periksa form untuk errors.')
    else:
        update_form = rusunForm(instance=update)

    isi = {
        'page_title': 'Detail Data Rumah Susun',
        'subjudul': 'Detail Data Rumah Susun',
        'post_form': update_form,
        'button': 'Edit',
    }

    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/')
def deleteRumah(request, pk):
    delete = get_object_or_404(GeoDataset, pk=pk)
        
    if request.method == 'POST':
        try:
            log_action(request, delete, DELETION, f'Menghapus Data: {delete}')
            delete.delete()
            messages.success(request, 'Data berhasil dihapus!')
        except Exception as e:
            messages.error(request, f'Gagal menghapus data: {str(e)}')

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/')
def deletePerumahan(request, pk):
    delete = get_object_or_404(Perumahan, pk=pk)
    
    if request.method == 'POST':
        try:
            for rumah in delete.rumah_set.all():
                if rumah.geo:
                    rumah.geo.delete()

            log_action(request, delete, DELETION, f'Menghapus Data: {delete}')
            delete.delete()
            messages.success(request, 'Data berhasil dihapus!')
        except Exception as e:
            messages.error(request, f'Gagal menghapus data: {str(e)}')

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/')
def deleteRusun(request, pk):
    delete = get_object_or_404(RumahSusun, pk=pk)
        
    if request.method == 'POST':
        try:
            log_action(request, delete, DELETION, f'Menghapus Data: {delete}')
            delete.delete()
            messages.success(request, 'Data berhasil dihapus!')
        except Exception as e:
            messages.error(request, f'Gagal menghapus data: {str(e)}')

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login')
def pengajuan(request):
    pengajuan_rumah_baru = AddRequest.objects.filter(disetujui=False, ditolak=False).count()
    pengajuan_rumah_ditolak = AddRequest.objects.filter(ditolak=True).count()
    perubahan_unit_rumah = UpdateRequest.objects.filter(disetujui=False, ditolak=False).count()

    isi = {
	'page_title': 'Pengajuan',
    'subjudul': 'Pengajuan',
    'pengajuan_rumah_baru': pengajuan_rumah_baru,
    'pengajuan_rumah_ditolak': pengajuan_rumah_ditolak,
    'perubahan_unit_rumah': perubahan_unit_rumah,
    }
    return render(request,'administrators/pengajuan.html', isi)

@login_required(login_url='/login')
def viewAddRequestRumah(request):
    search_query = request.GET.get('search', '')
    
    queryset = AddRequest.objects.filter(disetujui=False, ditolak=False)

    if search_query:
        queryset = queryset.filter(
            Q(dibuat_oleh__username__icontains=search_query)
        )

    table = AddRequestRumahTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Pembuat...'
    isi = {
        'placeholder_search' : placeholder_search,
        'table': table,
        'page_title': 'Pengajuan Tambah Unit Rumah',
        'subjudul': 'Pengajuan Tambah Unit Rumah',
    }
    return render(request, 'administrators/table_view.html', isi)

@login_required(login_url='/login')
def viewAddRequestRumahDitolak(request):
    search_query = request.GET.get('search', '')
    
    queryset = AddRequest.objects.filter(ditolak=True)

    if search_query:
        queryset = queryset.filter(
            Q(dibuat_oleh__username__icontains=search_query)
        )

    table = AddRequestRumahTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Pembuat...'
    isi = {
        'placeholder_search' : placeholder_search,
        'table': table,
        'page_title': 'Pengajuan Tambah Unit Rumah',
        'subjudul': 'Pengajuan Tambah Unit Rumah',
    }
    return render(request, 'administrators/table_view.html', isi)

@login_required(login_url='/login')
def addRequestRumah(request):    
    if request.method == 'POST':
        post_form = RumahAddRequestForm(request.POST, request.FILES)
        if post_form.is_valid():
            try:
                rumah_obj = post_form.save(commit=False)
                rumah_obj.dibuat_oleh = request.user
                rumah_obj.save()
                log_action(request, rumah_obj, ADDITION, f'Menambahkan Data: {rumah_obj}')
                messages.success(request, 'Berhasil Mengajukan Data Rumah!')
                post_form = RumahAddRequestForm()
            except Exception as e:
                messages.error(request, f'Gagal Untuk Mengajukan Data Rumah: {str(e)}')
    else:
        post_form = RumahAddRequestForm()

    isi = {
        'page_title': 'Pengajuan Tambah Rumah',
        'subjudul': 'Pengajuan Tambah Rumah',
        'post_form': post_form,
        'button': 'Simpan'
    }
    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/')
def prosesRequestRumah(request, pk):
    add_request = get_object_or_404(AddRequest, pk=pk)
    aksi = request.GET.get('aksi')

    if add_request.disetujui or add_request.ditolak:
        messages.warning(request, "Pengajuan ini sudah diproses sebelumnya.")
        return redirect('nama_view_daftar_request')

    if aksi == 'tolak':
        add_request.ditolak = True
        add_request.save()
        messages.info(request, "Pengajuan berhasil ditolak.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    elif aksi == 'setuju':
        data = add_request.data or {}
        nama_perumahan = data.get('nama_perumahan')
        perumahan = Perumahan.objects.filter(nama_perumahan=nama_perumahan).first()

        if not (nama_perumahan and add_request.geometry and perumahan):
            messages.error(request, "Data tidak lengkap atau perumahan tidak ditemukan.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        geo_dataset = GeoDataset.objects.create(
            nama_dataset=data.get('nama_pemilik', 'Tanpa Nama'),
            geometry=add_request.geometry,
            kategori='Unit Rumah',
            properties={"sumber": "form"}
        )

        Rumah.objects.create(
            nama_pemilik=data.get('nama_pemilik', 'Tanpa Nama'),
            alamat_rumah=data.get('alamat_rumah', '-'),
            rumah_sewa=data.get('rumah_sewa', False),
            jumlah_kk=data.get('jumlah_kk', 1),
            nilai_keselamatan=data.get('nilai_keselamatan'),
            nilai_kesehatan=data.get('nilai_kesehatan'),
            nilai_komponen=data.get('nilai_komponen'),
            status_rumah=data.get('status_rumah', 'RUMAH_LAYAK_HUNI'),
            status_luas=data.get('status_luas', 'LUAS_RUMAH_CUKUP'),
            geo=geo_dataset,
            nama_perumahan=perumahan,
            photo_rumah=add_request.photo_rumah,
        )

        add_request.disetujui = True
        add_request.save()

        messages.success(request, "Pengajuan disetujui dan data berhasil disimpan.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        messages.error(request, "Aksi tidak valid.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/') 
def updateRequestRumah(request, pk): 
    geo_instance = get_object_or_404(GeoDataset, pk=pk)
    
    try:
        rumah_instance = geo_instance.rumah
    except Rumah.DoesNotExist:
        rumah_instance = Rumah(geo=geo_instance)

    if request.method == "POST":
        # SIMPAN salinan awal sebelum diubah oleh form
        geo_initial = {field: getattr(geo_instance, field) for field in geoForm().fields}
        rumah_initial = {field: getattr(rumah_instance, field) for field in rumahForm().fields}

        geo_form = geoForm(request.POST, instance=geo_instance)
        rumah_form = rumahForm(request.POST, request.FILES, instance=rumah_instance)

        if geo_form.is_valid() and rumah_form.is_valid():
            perubahan = {}

            # Bandingkan GeoDataset
            for field in geo_form.cleaned_data:
                new = geo_form.cleaned_data[field]
                old = geo_initial[field]
                if str(new) != str(old):
                    perubahan[field] = str(new)

            # Bandingkan Rumah
            for field in rumah_form.cleaned_data:
                new = rumah_form.cleaned_data[field]
                old = rumah_initial[field]
                if str(new) != str(old):
                    # Simpan perubahan file ke UpdateRequest, URL-nya disimpan ke perubahan
                    if field == 'photo_rumah':
                        perubahan['photo_rumah_url'] = ''  # placeholder sementara
                    else:
                        perubahan[field] = str(new)

            if perubahan:
                # Simpan dulu instance UpdateRequest tanpa `data`
                ur = UpdateRequest.objects.create(
                    id_rumah=rumah_instance,
                    photo_rumah=rumah_form.cleaned_data.get('photo_rumah'),
                    geometry=geo_instance.geometry,
                    dibuat_oleh=request.user
                )

                # Perbarui URL gambar jika ada perubahan photo_rumah
                if 'photo_rumah_url' in perubahan and ur.photo_rumah:
                    perubahan['photo_rumah_url'] = ur.photo_rumah.url

                ur.data = perubahan
                ur.save()

                messages.success(request, "Permintaan perubahan berhasil diajukan.")
            else:
                messages.info(request, "Tidak ada perubahan yang terdeteksi.")

            return redirect('administrators:request-update-rumah', pk=pk)

    else:
        geo_form = geoForm(instance=geo_instance)
        rumah_form = rumahForm(instance=rumah_instance)

    isi = {
        'page_title': 'Detail Data Rumah',
        'subjudul': 'Detail Data Rumah',
        'post_form': rumah_form,
        'geo_form': geo_form,
        'button': 'Ajukan Perubahan',
    }

    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login')
def viewUpdateRequestRumah(request):
    search_query = request.GET.get('search', '')
    
    queryset = UpdateRequest.objects.filter(disetujui=False, ditolak=False)

    if search_query:
        queryset = queryset.filter(
            Q(dibuat_oleh__username__icontains=search_query) |
            Q(dibuat_oleh_users__icontains=search_query)
        )

    table = UpdateRequestRumahTable(queryset)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    placeholder_search = 'Cari Nama Pembuat...'
    isi = {
        'placeholder_search' : placeholder_search,
        'table': table,
        'page_title': 'Pengajuan Perubahan Unit Rumah',
        'subjudul': 'Pengajuan Perubahan Unit Rumah',
    }
    return render(request, 'administrators/table_view.html', isi)

