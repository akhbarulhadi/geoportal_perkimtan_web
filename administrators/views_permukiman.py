from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from gis_data.models import Rumah, Perumahan, RumahSusun
from .table import PerumahanTable, RusunTable, GeoDatasetTable
from .forms import rumahForm, perumahanForm, kelurahanForm, kecamatanForm, rusunForm, geoForm
from django.contrib import messages
from django_tables2 import RequestConfig
from maps.models import GeoDataset
from django.db.models import Q
from .logger import log_action
from django.contrib.admin.models import DELETION, ADDITION, CHANGE


@login_required(login_url='/login')
def pp(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
    'admin': admin,
    'operator': operator,
    }
    return render(request,'administrators/pp.html', isi)


@login_required(login_url='/login')
def unitRumah(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    # blocked_groups = ['admin']
    # if request.user.groups.filter(name__in=blocked_groups).exists():
    #     raise PermissionDenied
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
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/table_view.html', isi)


@login_required(login_url='/login')
def RLH(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'admin': admin,
        'operator': operator,
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def RTLH(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'admin': admin,
        'operator': operator,
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def rumahSewa(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'admin': admin,
        'operator': operator,
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def perumahan(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'admin': admin,
        'operator': operator,
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def perumahanSubsidi(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'admin': admin,
        'operator': operator,
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def rumahSubsidi(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'admin': admin,
        'operator': operator,
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def rumahSusun(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'admin': admin,
        'operator': operator,
    }
    return render(request,'administrators/table_view.html', isi)

@login_required(login_url='/login')
def addRumah(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    if request.method == 'POST':
        geo_form = geoForm(request.POST, request.FILES)
        rumah_form = rumahForm(request.POST, request.FILES)

        if geo_form.is_valid() and rumah_form.is_valid():
            try:
                rumah_obj = rumah_form.save(commit=False)
                perumahan = rumah_obj.nama_perumahan
                kecamatan = perumahan.kecamatan.kecamatan if perumahan else "Tanpa Kecamatan"

                geo_obj = geo_form.save(commit=False)
                geo_obj.nama_dataset=kecamatan
                geo_obj.kategori="Unit Rumah"
                geo_obj.properties={"sumber": "form"}
                geo_obj.save()

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
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login')
def addPerumahan(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'button': 'Simpan',
        'admin': admin,
        'operator': operator,
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
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'button': 'Simpan',
        'admin': admin,
        'operator': operator,
    }
    return render(request, 'administrators/forms.html', isi)




@login_required(login_url='/login') 
def updateRumah(request, pk):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
                rumah_obj = rumah_form.save(commit=False)
                perumahan = rumah_obj.nama_perumahan
                kecamatan = perumahan.kecamatan.kecamatan if perumahan else "Tanpa Kecamatan"

                geo_obj = geo_form.save(commit=False)
                geo_obj.nama_dataset = kecamatan  # update nama_dataset berdasarkan kecamatan
                geo_obj.save()

                rumah_obj.geo = geo_obj
                rumah_obj.save()
                
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
        'admin': admin,
        'operator': operator,
    }

    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login') 
def updatePerumahan(request, pk):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'admin': admin,
        'operator': operator,
    }

    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login') 
def updateRusun(request, pk):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

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
        'admin': admin,
        'operator': operator,
    }

    return render(request, 'administrators/forms.html', isi)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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
def preview_data_rumah_pdf(request, pk): # <= Nama fungsi diubah
    geo_instance = get_object_or_404(GeoDataset, pk=pk)

    try:
        rumah = geo_instance.rumah
    except Rumah.DoesNotExist:
        return HttpResponse("Data rumah tidak ditemukan", status=404)

    perumahan = rumah.nama_perumahan
    kecamatan = perumahan.kecamatan.kecamatan if perumahan and perumahan.kecamatan else 'Tanpa Kecamatan'

    context = {
        'rumah': rumah,
        'geo': geo_instance,
        'perumahan': perumahan,
        'kecamatan': kecamatan,
    }

    return render(request, 'administrators/pdf_rumah.html', context)