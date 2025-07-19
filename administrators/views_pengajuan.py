from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from gis_data.models import Rumah, Perumahan, AddRequest, UpdateRequest
from .table import AddRequestRumahTable, UpdateRequestRumahTable, GeoDatasetTable
from .forms import rumahForm, geoForm, RumahAddRequestForm
from django.contrib import messages
from django_tables2 import RequestConfig
from maps.models import GeoDataset
from django.db.models import Q
from .logger import log_action
from django.contrib.admin.models import ADDITION, DELETION, CHANGE
from django.db import models

@login_required(login_url='/login')
def pengajuan(request):
    permission_admin = ['admin']
    permission_operator = ['operator']
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    if admin:
        # Admin bisa lihat semua data
        pengajuan_rumah_baru = AddRequest.objects.filter(disetujui=False, ditolak=False).count()
        pengajuan_rumah_ditolak = AddRequest.objects.filter(ditolak=True).count()
        pengajuan_rumah_disetujui = AddRequest.objects.filter(disetujui=True).count()
        perubahan_unit_rumah = UpdateRequest.objects.filter(disetujui=False, ditolak=False).count()
        perubahan_unit_rumah_ditolak = UpdateRequest.objects.filter(ditolak=True).count()
        perubahan_unit_rumah_disetujui = UpdateRequest.objects.filter(disetujui=True).count()
        penghapusan_rumah = GeoDataset.objects.filter(kategori='Unit Rumah', is_delete=True).count()
    elif operator:
        # Operator hanya bisa lihat data buatannya sendiri
        pengajuan_rumah_baru = AddRequest.objects.filter(disetujui=False, ditolak=False, dibuat_oleh=request.user).count()
        pengajuan_rumah_ditolak = AddRequest.objects.filter(ditolak=True, dibuat_oleh=request.user).count()
        pengajuan_rumah_disetujui = AddRequest.objects.filter(disetujui=True, dibuat_oleh=request.user).count()
        perubahan_unit_rumah = UpdateRequest.objects.filter(disetujui=False, ditolak=False, dibuat_oleh=request.user).count()
        perubahan_unit_rumah_ditolak = UpdateRequest.objects.filter(ditolak=True, dibuat_oleh=request.user).count()
        perubahan_unit_rumah_disetujui = UpdateRequest.objects.filter(disetujui=True, dibuat_oleh=request.user).count()
        penghapusan_rumah = GeoDataset.objects.filter(kategori='Unit Rumah', is_delete=True, dibuat_oleh=request.user).count()
    else:
        # Default fallback: tidak ada data
        pengajuan_rumah_baru = 0
        pengajuan_rumah_ditolak = 0
        pengajuan_rumah_disetujui = 0
        perubahan_unit_rumah = 0
        perubahan_unit_rumah_ditolak = 0
        perubahan_unit_rumah_disetujui = 0
        penghapusan_rumah = 0

    isi = {
        'page_title': 'Pengajuan',
        'subjudul': 'Pengajuan',
        'pengajuan_rumah_baru': pengajuan_rumah_baru,
        'pengajuan_rumah_ditolak': pengajuan_rumah_ditolak,
        'pengajuan_rumah_disetujui': pengajuan_rumah_disetujui,
        'perubahan_unit_rumah': perubahan_unit_rumah,
        'perubahan_unit_rumah_ditolak': perubahan_unit_rumah_ditolak,
        'perubahan_unit_rumah_disetujui': perubahan_unit_rumah_disetujui,
        'penghapusan_rumah': penghapusan_rumah,
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/pengajuan.html', isi)


@login_required(login_url='/login')
def viewAddRequestRumah(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    search_query = request.GET.get('search', '')

    if admin:
        # Admin melihat semua pengajuan
        queryset = AddRequest.objects.filter(disetujui=False, ditolak=False)
    elif operator:
        # Operator hanya melihat pengajuan miliknya sendiri
        queryset = AddRequest.objects.filter(disetujui=False, ditolak=False, dibuat_oleh=request.user)
    else:
        # Fallback: tidak bisa melihat apa-apa
        queryset = AddRequest.objects.none()

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
        'page_title': 'Tambah Rumah Baru',
        'subjudul': 'Tambah Rumah Baru',
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/table_view.html', isi)

@login_required(login_url='/login')
def viewAddRequestRumahDitolak(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    search_query = request.GET.get('search', '')

    if admin:
        # Admin melihat semua pengajuan
        queryset = AddRequest.objects.filter(ditolak=True)
    elif operator:
        # Operator hanya melihat pengajuan miliknya sendiri
        queryset = AddRequest.objects.filter(ditolak=True, dibuat_oleh=request.user)
    else:
        # Fallback: tidak bisa melihat apa-apa
        queryset = AddRequest.objects.none()

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
        'page_title': 'Tambah Rumah Yang Di Tolak',
        'subjudul': 'Tambah Rumah Yang Di Tolak',
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/table_view.html', isi)

@login_required(login_url='/login')
def viewAddRequestRumahDisetujui(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    search_query = request.GET.get('search', '')

    if admin:
        # Admin melihat semua pengajuan
        queryset = AddRequest.objects.filter(disetujui=True)
    elif operator:
        # Operator hanya melihat pengajuan miliknya sendiri
        queryset = AddRequest.objects.filter(disetujui=True, dibuat_oleh=request.user)
    else:
        # Fallback: tidak bisa melihat apa-apa
        queryset = AddRequest.objects.none()

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
        'page_title': 'Tambah Rumah Yang Di Setujui',
        'subjudul': 'Tambah Rumah Yang Di Setujui',
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/table_view.html', isi)

@login_required(login_url='/login')
def addRequestRumah(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    if request.method == 'POST':
        post_form = RumahAddRequestForm(request.POST, request.FILES)
        if post_form.is_valid():
            try:
                rumah_obj = post_form.save(commit=False)
                rumah_obj.dibuat_oleh = request.user
                rumah_obj.save()
                log_action(request, rumah_obj, ADDITION, f'Mengajukan Penambahan Data: {rumah_obj}')
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
        'button': 'Simpan',
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login')
def prosesAddRequestRumah(request, pk):
    add_request = get_object_or_404(AddRequest, pk=pk)
    aksi = request.GET.get('aksi')

    if add_request.disetujui or add_request.ditolak:
        messages.warning(request, "Pengajuan ini sudah diproses sebelumnya.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if aksi == 'tolak':
        add_request.ditolak = True
        add_request.save()
        log_action(request, add_request, CHANGE, f'Menolak Pengajuan Data Baru: {add_request}')
        messages.info(request, "Pengajuan berhasil ditolak.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    elif aksi == 'setuju':
        data = add_request.data or {}
        nama_perumahan = data.get('nama_perumahan')
        perumahan = Perumahan.objects.filter(nama_perumahan=nama_perumahan).first()

        if not (nama_perumahan and add_request.geometry and perumahan):
            messages.error(request, "Data tidak lengkap atau perumahan tidak ditemukan.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
        kecamatan = perumahan.kecamatan.kecamatan if perumahan and perumahan.kecamatan else 'Tanpa Nama'

        geo_dataset = GeoDataset.objects.create(
            nama_dataset=kecamatan,
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
            status_rumah=data.get('status_rumah'),
            status_luas=data.get('status_luas'),
            geo=geo_dataset,
            nama_perumahan=perumahan,
            photo_rumah=add_request.photo_rumah,
            dibuat_oleh_users=add_request.dibuat_oleh_users
        )

        add_request.disetujui = True
        add_request.save()
        log_action(request, add_request, CHANGE, f'Setujui Pengajuan Data Baru: {add_request}')
        messages.success(request, "Pengajuan disetujui dan data berhasil disimpan.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        messages.error(request, "Aksi tidak valid.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/login') 
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
                    # elif field == 'nama_perumahan':
                    #     # Simpan sebagai field 'perumahan' dengan ID
                    #     perubahan['perumahan'] = new.id_perumahan if new else None
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
                log_action(request, ur, ADDITION, f'Mengajukan Perubahan Data: {ur}')
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
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    search_query = request.GET.get('search', '')

    if admin:
        # Admin melihat semua pengajuan
        queryset = UpdateRequest.objects.filter(disetujui=False, ditolak=False)
    elif operator:
        # Operator hanya melihat pengajuan miliknya sendiri
        queryset = UpdateRequest.objects.filter(disetujui=False, ditolak=False, dibuat_oleh=request.user)
    else:
        # Fallback: tidak bisa melihat apa-apa
        queryset = UpdateRequest.objects.none()
        
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
        'page_title': 'Perubahan Unit Rumah',
        'subjudul': 'Perubahan Unit Rumah',
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/table_view.html', isi)

@login_required(login_url='/login')
def viewUpdateRequestRumahDitolak(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    search_query = request.GET.get('search', '')

    if admin:
        # Admin melihat semua pengajuan
        queryset = UpdateRequest.objects.filter(ditolak=True)
    elif operator:
        # Operator hanya melihat pengajuan miliknya sendiri
        queryset = UpdateRequest.objects.filter(ditolak=True, dibuat_oleh=request.user)
    else:
        # Fallback: tidak bisa melihat apa-apa
        queryset = UpdateRequest.objects.none()

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
        'page_title': 'Perubahan Unit Rumah Yang Di Tolak',
        'subjudul': 'Perubahan Unit Rumah Yang Di Tolak',
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/table_view.html', isi)

@login_required(login_url='/login')
def viewUpdateRequestRumahDisetujui(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    search_query = request.GET.get('search', '')

    if admin:
        # Admin melihat semua pengajuan
        queryset = UpdateRequest.objects.filter(disetujui=True)
    elif operator:
        # Operator hanya melihat pengajuan miliknya sendiri
        queryset = UpdateRequest.objects.filter(disetujui=True, dibuat_oleh=request.user)
    else:
        # Fallback: tidak bisa melihat apa-apa
        queryset = UpdateRequest.objects.none()

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
        'page_title': 'Perubahan Unit Rumah Yang Di Setujui',
        'subjudul': 'Perubahan Unit Rumah Yang Di Setujui',
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/table_view.html', isi)

@login_required(login_url='/login')
def prosesUpdateRequestRumah(request, pk):
    ur = get_object_or_404(UpdateRequest, pk=pk)
    aksi = request.GET.get('aksi')

    # Cegah pemrosesan ulang
    if ur.disetujui or ur.ditolak:
        messages.warning(request, "Permintaan ini sudah diproses sebelumnya.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Aksi tolak
    if aksi == 'tolak':
        ur.ditolak = True
        ur.save()
        log_action(request, ur, CHANGE, f'Menolak Pengajuan Perubahan: {ur}')
        messages.info(request, "Permintaan berhasil ditolak.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Aksi setuju
    elif aksi == 'setuju':
        rumah = ur.id_rumah
        geo = rumah.geo
        perubahan = ur.data or {}

        # Update GeoDataset jika ada perubahan geometry
        if 'geometry' in perubahan:
            geo.geometry = ur.geometry
            geo.save()

        # Update Rumah
        for field, value in perubahan.items():
            if field == 'photo_rumah_url':
                continue  # hanya preview
            if hasattr(rumah, field):
                field_obj = Rumah._meta.get_field(field)

                # Konversi ke tipe data field yang sesuai
                if isinstance(field_obj, models.BooleanField):
                    value = value in ['True', 'true', '1']
                elif isinstance(field_obj, models.IntegerField):
                    value = int(value)
                elif isinstance(field_obj, models.ForeignKey):
                    if field == 'nama_perumahan': 
                        try:
                            perumahan = Perumahan.objects.get(nama_perumahan=value)
                            value = perumahan
                        except Perumahan.DoesNotExist:
                            messages.error(request, "Perumahan dengan ID tersebut tidak ditemukan.")
                            return redirect(request.META.get('HTTP_REFERER', '/'))

                setattr(rumah, field, value)

        # Update foto jika ada
        if ur.photo_rumah:
            rumah.photo_rumah = ur.photo_rumah

        # Update foto jika ada
        if ur.dibuat_oleh_users:
            rumah.dibuat_oleh_users = ur.dibuat_oleh_users

        # Tambahan: update nama_dataset berdasarkan kecamatan
        if 'nama_perumahan' in perubahan and rumah.geo:
            try:
                perumahan = Perumahan.objects.get(nama_perumahan=perubahan['nama_perumahan'])
                nama_kecamatan = perumahan.kecamatan.kecamatan
                rumah.geo.nama_dataset = nama_kecamatan
                rumah.geo.save()
            except Perumahan.DoesNotExist:
                messages.error(request, "Perumahan tidak ditemukan saat update nama_dataset.")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
        rumah.save()

        # Tandai permintaan sebagai disetujui
        ur.disetujui = True
        ur.save()
        log_action(request, ur, CHANGE, f'Setujui Pengajuan Perubahan: {ur}')
        messages.success(request, "Perubahan berhasil disetujui dan diterapkan.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        messages.error(request, "Aksi tidak valid.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
@login_required(login_url='/login')
def requestDeleteRumah(request, pk):
    dataset = get_object_or_404(GeoDataset, pk=pk)
        
    if request.method == 'POST':
        try:
            dataset.is_delete = True
            dataset.dibuat_oleh = request.user
            dataset.save()
            log_action(request, dataset, CHANGE, f'Mengajukan Penghapusan Data: {dataset}')
            messages.success(request, 'Penghapusan Data Berhasil Diajukan!')
        except Exception as e:
            messages.error(request, f'Gagal mengajukan hapus data: {str(e)}')

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/login')
def viewRequestDeleteRumah(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    search_query = request.GET.get('search', '')
    if admin:
        queryset = GeoDataset.objects.select_related('rumah').filter(kategori='Unit Rumah', is_delete=True).order_by('rumah__nama_pemilik')
    elif operator:
        queryset = GeoDataset.objects.select_related('rumah').filter(kategori='Unit Rumah', is_delete=True, dibuat_oleh=request.user).order_by('rumah__nama_pemilik')
    else:
        queryset = GeoDataset.objects.none()

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
        'page_title': 'Penghapusan Unit Rumah',
        'subjudul': 'Penghapusan Unit Rumah',
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/table_view.html', isi)

@login_required(login_url='/login')
def prosesDeleteRequstRumah(request, pk):
    aksi = request.GET.get('aksi')
    dataset = get_object_or_404(GeoDataset, pk=pk)

    if aksi == 'setuju':
        try:
            log_action(request, dataset, DELETION, f'Setujui Penghapusan Data: {dataset}')
            dataset.delete()
            messages.success(request, 'Data berhasil dihapus!')
        except Exception as e:
            messages.error(request, f'Gagal menghapus data: {str(e)}')

    elif aksi == 'tolak':
        try:
            dataset.is_delete = False
            dataset.save()
            log_action(request, dataset, CHANGE, f'Tolak Penghapusan Data: {dataset}')
            messages.success(request, 'Permintaan penghapusan ditolak.')
        except Exception as e:
            messages.error(request, f'Gagal menolak permintaan: {str(e)}')

    else:
        messages.error(request, 'Aksi tidak dikenali.')

    return redirect(request.META.get('HTTP_REFERER', '/'))