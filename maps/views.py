from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import GarisPantai, KawasanKumuh, JalanLingkungan, Maps, DataMaps, FieldMaps
from django.contrib.gis.serializers import geojson
from gis_data.models import Rumah, Kecamatan, Kelurahan, AddRequest, UpdateRequest
from administrators.table import RumahTable
from .forms import mapsForm
from django.contrib import messages
from django.conf import settings
import json
import os
import geopandas as gpd
from .forms import GeoJSONUploadForm, GeoJSONUploadUnitRumahForm
from .models import GeoDataset, UploadProgress
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import F
from django.core.serializers import serialize
from django.utils.safestring import mark_safe
from django.http import JsonResponse
import threading
from uuid import uuid4
from types import SimpleNamespace
from django.contrib.auth.models import User
from administrators.logger import log_action  # atau lokasi file log kamu
from django.contrib.admin.models import ADDITION

# Create your views here.

@login_required(login_url='/login')
def pp(request):

    isi = {
	'page_title': 'Peta Permukiman',
    'subjudul': 'Peta Permukiman',
    }
    return render(request,'maps/index.html', isi)

@login_required(login_url='/login')
def datasets(request):
    maps = GeoDataset.objects.exclude(kategori='Unit Rumah').values('kategori').distinct()
    maps_unit_rumah = GeoDataset.objects.filter(kategori='Unit Rumah').values('kategori').distinct()

    isi = {
	'page_title': 'Maps',
    'subjudul': 'Maps',
    'maps': maps,
    'maps_unit_rumah': maps_unit_rumah,
    'icon_button_map': 'addmap',
    'icon_button_house': 'addhouse',
    'button_map': 'Tambah Map',
    'button_house': 'Tambah House',
    }
    return render(request,'maps/index2.html', isi)

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
def addMap(request):
    post_form = mapsForm(request.POST, request.FILES)
    if request.method == 'POST':
      if post_form.is_valid():
        try:
          post_form.save()
          messages.success(request, 'Berhasil Menambahkan Data Map!')
          post_form = mapsForm()
        except Exception as e:
            messages.error(request, f'Gagal Untuk Menambahkan Data Map: {str(e)}')
      else:
          messages.error(request, 'Gagal Untuk Menambahkan Data Map. Periksa form untuk errors.')
    isi = {
	'page_title': 'Tambah Map',
    'subjudul': 'Tambah Map',
    'post_form': post_form,
    'button': 'Simpan',
    }
    return render(request,'administrators/forms.html', isi)

@login_required(login_url='/')
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

@login_required(login_url='/login')
def garis_pantai_view(request):
    garis_pantai = geojson.Serializer().serialize(GarisPantai.objects.all())

    isi = {
        'page_title': 'Batas Garis Pantai Kota Batam',
        'subjudul': 'Batas Garis Pantai Kota Batam',
        'data_map': garis_pantai,

    }
    return render(request, 'maps/map3.html', isi)

@login_required(login_url='/login')
def kawasan_kumuh_view(request):
    kawasan_kumuh = geojson.Serializer().serialize(KawasanKumuh.objects.all())

    isi = {
        'page_title': 'Kawasan Kumuh Kota Batam',
        'subjudul': 'Kawasan Kumuh Kota Batam',
        'data_map': kawasan_kumuh,

    }
    return render(request, 'maps/map3.html', isi)

@login_required(login_url='/login')
def jalan_lingkungan_view(request):
    jalan_lingkungan = geojson.Serializer().serialize(JalanLingkungan.objects.all())

    isi = {
        'page_title': 'Jalan Lingkungan Kota Batam',
        'subjudul': 'Jalan Lingkungan Kota Batam',
        'data_map': jalan_lingkungan,

    }
    return render(request, 'maps/map3.html', isi)

@login_required(login_url='/login')
def rumah_view(request):
    rumah = geojson.Serializer().serialize(
        Rumah.objects.exclude(lokasi_rumah__isnull=True), 
        geometry_field="lokasi_rumah",
    )
    queryset = Rumah.objects.all()
    table = RumahTable(queryset)
    isi = {
        'page_title': 'Unit Rumah Kota Batam',
        'subjudul': 'Unit Rumah Kota Batam',
        'data_map': rumah,
        'table': table,

    }
    return render(request, 'maps/map3.html', isi)

@login_required(login_url='/login')
def peta_geojson(request):
    geojson_path = os.path.join(settings.BASE_DIR, 'data', 'LUBUK_BAJA.geojson')
    
    with open(geojson_path, encoding='utf-8') as f:
        geojson_data = json.load(f)

    context = {
        'page_title': 'Peta Dinamis GeoJSON',
        'data_map': json.dumps(geojson_data),
    }
    return render(request, 'maps/map_geojson.html', context)

# @login_required(login_url='/login')
# def peta_geojson(request):
#     # Path ke file SHP
#     shp_path = os.path.join(settings.BASE_DIR, 'data/Kota_Batam', 'Kota_Batam.shp')
    
#     # Baca shapefile pakai GeoPandas
#     gdf = gpd.read_file(shp_path)

#     # Pastikan CRS-nya WGS84 (Leaflet pakai EPSG:4326)
#     if gdf.crs != "EPSG:4326":
#         gdf = gdf.to_crs(epsg=4326)

#     # Konversi ke GeoJSON
#     geojson_data = gdf.to_json()

#     context = {
#         'page_title': 'Peta Dinamis dari SHP',
#         'data_map': geojson_data,  # Tidak perlu json.dumps lagi, karena sudah string JSON
#     }
#     return render(request, 'maps/map_geojson.html', context)

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

def upload_geojson(request):
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
        'upload_url_name': 'maps:upload-geojson'
    }
    return render(request, "maps/upload_geojson.html", isi)

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
def upload_geojson_unit_rumah(request):
    if request.method == 'POST':
        form = GeoJSONUploadUnitRumahForm(request.POST, request.FILES)
        if form.is_valid():
            task_id = str(uuid4())  # generate unique ID
            UploadProgress.objects.create(task_id=task_id, progress=0)

            geo_file = form.cleaned_data["file"]
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
                            kategori='Unit Rumah',
                            geometry=geom,
                            properties=props
                        )
                        log_action(SimpleNamespace(user=user), geo_obj, ADDITION, f'Menambahkan Data: {geo_obj}')
                        UploadProgress.objects.filter(task_id=task_id).update(progress=int((i+1)/total * 100))
                    UploadProgress.objects.filter(task_id=task_id).update(status="done")
                except Exception:
                    UploadProgress.objects.filter(task_id=task_id).update(status="failed")

            threading.Thread(target=process_data).start()

            return JsonResponse({"task_id": task_id})
        return JsonResponse({"error": "Form tidak valid"}, status=400)
    
    form = GeoJSONUploadUnitRumahForm()

    isi = {
        'form': form,
        'page_title': 'Upload Unit Rumah',
        'subjudul': 'Upload Unit Rumah',
        'upload_url_name': 'maps:upload-unit-rumah-geojson'
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
