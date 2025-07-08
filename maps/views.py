from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from gis_data.models import Rumah, AddRequest, UpdateRequest, Kecamatan
from django.contrib import messages
import json
from .forms import GeoJSONUploadForm, GeoJSONUploadUnitRumahForm
from .models import GeoDataset, UploadProgress
from django.contrib.gis.geos import GEOSGeometry
from django.utils.safestring import mark_safe
from django.http import JsonResponse
import threading
from uuid import uuid4
from types import SimpleNamespace
from django.contrib.auth.models import User
from administrators.logger import log_action
from django.contrib.admin.models import ADDITION
from django.db.models import Count

# Create your views here.

@login_required(login_url='/login')
def datasets(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    maps = GeoDataset.objects.exclude(kategori='Unit Rumah').values('kategori').distinct()
    maps_unit_rumah = GeoDataset.objects.filter(kategori='Unit Rumah').values('kategori').distinct()
    jumlah_unit_rumah = GeoDataset.objects.filter(kategori="Unit Rumah").count()

    kecamatans = Kecamatan.objects.values_list('kecamatan', flat=True)
    counts = GeoDataset.objects.values('nama_dataset').annotate(jumlah=Count('id'))
    jumlah_dict = {item['nama_dataset']: item['jumlah'] for item in counts}
    kecamatan = []
    for nama in kecamatans:
        kecamatan.append({
            'kecamatan': nama,
            'jumlah_data_rumah_perfilter': jumlah_dict.get(nama, 0)
        })

    isi = {
	    'page_title': 'Maps',
        'subjudul': 'Maps',
        'maps': maps,
        'maps_unit_rumah': maps_unit_rumah,
        'jumlah_unit_rumah': jumlah_unit_rumah,
        'kecamatan': kecamatan,
        'icon_button_map': 'addmap',
        'icon_button_house': 'addhouse',
        'button_map': 'Tambah Map',
        'button_house': 'Tambah House',
        'admin': admin,
        'operator': operator,
    }
    return render(request,'maps/index.html', isi)

@login_required(login_url='/login')
def maps(request, kategori):
    queryset = GeoDataset.objects.exclude(kategori='Unit Rumah').filter(kategori=kategori)

    features = []
    for obj in queryset:
        geom = json.loads(obj.geometry.geojson)
        features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": {"id": obj.id}  # hanya kirim ID
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    isi = {
        'page_title': 'Maps',
        'subjudul': f'Data kategori: {kategori}',
        'kategori': kategori,
        'data_map': mark_safe(json.dumps(geojson))
    }
    return render(request, 'maps/maps.html', isi)

@login_required(login_url='/login')
def map_detail_json(request, pk):
    obj = get_object_or_404(GeoDataset, pk=pk)
    detail = {
        "kategori": obj.kategori,
        "nama_dataset": obj.nama_dataset,
    }
    detail.update(obj.properties)
    return JsonResponse(detail)

@login_required(login_url='/login')
def maps_unit_rumah(request, kategori):
    queryset = GeoDataset.objects.filter(kategori='Unit Rumah')

    features = []
    for obj in queryset:
        geom = json.loads(obj.geometry.geojson)
        features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": {"id": obj.id}  # hanya kirim ID
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    isi = {
        'page_title': 'Maps Unit Rumah',
        'subjudul': f'Data kategori: {kategori}',
        'kategori': kategori,
        'data_map': mark_safe(json.dumps(geojson))
    }
    return render(request, 'maps/maps_unit_rumah.html', isi)

@login_required(login_url='/login')
def map_detail_json_unit_rumah(request, pk):
    obj = get_object_or_404(GeoDataset, pk=pk)
    detail = {
        # "geometry": obj.geometry.geojson,
        # "kategori": obj.kategori,
        # "nama_dataset": obj.nama_dataset,
    }
    try:
        rumah = obj.rumah
        detail["rumah"] = {
            "nama_pemilik": rumah.nama_pemilik,
            "alamat_rumah": rumah.alamat_rumah,
            "rumah_sewa": rumah.rumah_sewa,
            "jumlah_kk": rumah.jumlah_kk,
            "nilai_keselamatan": rumah.nilai_keselamatan,
            "nilai_kesehatan": rumah.nilai_kesehatan,
            "nilai_komponen": rumah.nilai_komponen,
            "status_rumah": rumah.get_status_rumah_display(),
            "status_luas": rumah.get_status_luas_display(),
            "nama_perumahan": rumah.nama_perumahan.nama_perumahan,
            "kecamatan": str(rumah.nama_perumahan.kecamatan), 
            "kelurahan": str(rumah.nama_perumahan.kelurahan), 
            "photo_rumah_url": rumah.photo_rumah.url if rumah.photo_rumah else None,
        }
    except Rumah.DoesNotExist:
        detail["rumah"] = None

    detail.update({
        # "RT": obj.properties.get("RT"),
        # "RW": obj.properties.get("RW"),
        "Shape_Leng": obj.properties.get("Shape_Leng"),
    })
    return JsonResponse(detail)

@login_required(login_url='/login')
def deleteMaps(request, kategori):
    if request.method == 'POST':
        try:
            # Dapatkan semua data dengan kategori tersebut
            items = GeoDataset.objects.filter(kategori=kategori)
            if not items.exists():
                messages.warning(request, 'Tidak ada data yang ditemukan untuk dihapus.')
            else:
                items.delete()
                messages.success(request, 'Semua data dengan kategori tersebut berhasil dihapus!')
        except Exception as e:
            messages.error(request, f'Gagal menghapus data: {str(e)}')

    return redirect(request.META.get('HTTP_REFERER', '/'))

def remove_z(geometry):
    geom_type = geometry.get("type")
    coords = geometry.get("coordinates")

    if geom_type == "Point":
        coords = coords[:2]
    elif geom_type == "MultiPoint":
        coords = [point[:2] for point in coords]
    elif geom_type == "LineString":
        coords = [point[:2] for point in coords]
    elif geom_type == "MultiLineString":
        coords = [[point[:2] for point in line] for line in coords]
    elif geom_type == "Polygon":
        coords = [[point[:2] for point in ring] for ring in coords]
    elif geom_type == "MultiPolygon":
        coords = [[[point[:2] for point in ring] for ring in polygon] for polygon in coords]

    geometry["coordinates"] = coords
    return geometry

def check_progress(request, task_id):
    try:
        task = UploadProgress.objects.get(task_id=task_id)
        return JsonResponse({
            "progress": task.progress,
            "status": task.status
        })
    except UploadProgress.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

@login_required(login_url='/login')
def upload_geojson(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    if request.method == 'POST':
        form = GeoJSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            task_id = str(uuid4())
            UploadProgress.objects.create(task_id=task_id, progress=0)

            geo_file = form.cleaned_data["file"]
            kategori = form.cleaned_data["kategori"]
            geojson = json.load(geo_file)

            user_id = request.user.id

            def process_data(user_id):
                try:
                    user = User.objects.get(id=user_id)
                    total = len(geojson["features"])
                    for i, feat in enumerate(geojson["features"]):
                        geom_data = remove_z(feat["geometry"])
                        geom = GEOSGeometry(json.dumps(geom_data), srid=4326)
                        props = feat.get("properties", {})

                        geo_obj = GeoDataset.objects.create(
                            nama_dataset='1',
                            kategori=kategori,
                            geometry=geom,
                            properties=props
                        )
                        log_action(SimpleNamespace(user=user), geo_obj, ADDITION, f'Menambahkan Data: {geo_obj}')
                        UploadProgress.objects.filter(task_id=task_id).update(progress=int((i + 1) / total * 100))
                    UploadProgress.objects.filter(task_id=task_id).update(status="done")
                except Exception:
                    UploadProgress.objects.filter(task_id=task_id).update(status="failed")

            threading.Thread(target=process_data, args=(user_id,)).start()

            return JsonResponse({"task_id": task_id})
        return JsonResponse({"error": "Form tidak valid"}, status=400)

    form = GeoJSONUploadForm()
    kategori_list = GeoDataset.objects.exclude(kategori='Unit Rumah').order_by().values_list('kategori', flat=True).distinct()

    isi = {
        'form': form,
        'page_title': 'Upload',
        'subjudul': 'Upload',
        'kategori_list': kategori_list,
        'upload_url_name': 'maps:upload-geojson',
        'admin': admin,
        'operator': operator,
    }
    return render(request, "maps/upload_geojson.html", isi)

@login_required(login_url='/login')
def upload_geojson_unit_rumah(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    if request.method == 'POST':
        form = GeoJSONUploadUnitRumahForm(request.POST, request.FILES)
        if form.is_valid():
            task_id = str(uuid4())  # generate unique ID
            UploadProgress.objects.create(task_id=task_id, progress=0)

            geo_file = form.cleaned_data["file"]
            geojson = json.load(geo_file)
            nama_dataset = form.cleaned_data["nama_dataset"]

            user_id = request.user.id

            def process_data(user_id):
                try:
                    user = User.objects.get(id=user_id)
                    total = len(geojson["features"])
                    for i, feat in enumerate(geojson["features"]):
                        geom_data = remove_z(feat["geometry"])
                        geom = GEOSGeometry(json.dumps(geom_data), srid=4326)
                        props = feat.get("properties", {})

                        geo_obj = GeoDataset.objects.create(
                            nama_dataset=nama_dataset,
                            kategori='Unit Rumah',
                            geometry=geom,
                            properties=props
                        )
                        Rumah.objects.create(
                            geo=geo_obj
                        )
                        log_action(SimpleNamespace(user=user), geo_obj, ADDITION, f'Menambahkan Data: {geo_obj}')
                        UploadProgress.objects.filter(task_id=task_id).update(progress=int((i+1)/total * 100))
                    UploadProgress.objects.filter(task_id=task_id).update(status="done")
                except Exception:
                    UploadProgress.objects.filter(task_id=task_id).update(status="failed")

            threading.Thread(target=process_data, args=(user_id,)).start()

            return JsonResponse({"task_id": task_id})
        return JsonResponse({"error": "Form tidak valid"}, status=400)
    
    form = GeoJSONUploadUnitRumahForm()
    item_menu_filter = Kecamatan.objects.order_by().values_list('kecamatan', flat=True).distinct()

    isi = {
        'form': form,
        'page_title': 'Upload Unit Rumah',
        'subjudul': 'Upload Unit Rumah',
        'upload_url_name': 'maps:upload-unit-rumah-geojson',
        'item_menu_filter': item_menu_filter,
        'admin': admin,
        'operator': operator,
    }
    return render(request, "maps/upload_geojson.html", isi)

@login_required(login_url='/login')
def maps_object_add_rumah(request, pk):
    queryset = AddRequest.objects.filter(pk=pk)

    features = []
    for obj in queryset:
        geom = json.loads(obj.geometry.geojson)
        features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": {"id": obj.id}  # hanya kirim ID
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    isi = {
        'page_title': 'Maps',
        'subjudul': f'Data kategori: {pk}',
        'kategori': pk,
        'data_map': mark_safe(json.dumps(geojson))
    }
    return render(request, 'maps/maps_object_add_rumah.html', isi)

@login_required(login_url='/login')
def maps_object_add_rumah_detail_json(request, pk):
    obj = get_object_or_404(AddRequest, pk=pk)
    detail = {
        "photo_rumah_url": obj.photo_rumah.url if obj.photo_rumah else None,
        "photo_perumahan_url": obj.photo_perumahan.url if obj.photo_perumahan else None,
        "Dibuat oleh": str(obj.dibuat_oleh),
    }
    detail.update(obj.data)
    return JsonResponse(detail)

@login_required(login_url='/login')
def maps_object_update_rumah(request, pk):
    queryset = UpdateRequest.objects.filter(pk=pk)

    features = []
    for obj in queryset:
        geom = json.loads(obj.geometry.geojson)
        features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": {"id": obj.id}  # hanya kirim ID
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    isi = {
        'page_title': 'Maps',
        'subjudul': f'Data kategori: {pk}',
        'kategori': pk,
        'data_map': mark_safe(json.dumps(geojson))
    }
    return render(request, 'maps/maps_object_update_rumah.html', isi)

@login_required(login_url='/login')
def maps_object_update_rumah_detail_json(request, pk):
    obj = get_object_or_404(UpdateRequest, pk=pk)
    detail = {
        "photo_rumah_url": obj.photo_rumah.url if obj.photo_rumah else None,
        "photo_perumahan_url": obj.photo_perumahan.url if obj.photo_perumahan else None,
        "Dibuat oleh": str(obj.dibuat_oleh),
    }
    detail.update(obj.data)
    return JsonResponse(detail)
