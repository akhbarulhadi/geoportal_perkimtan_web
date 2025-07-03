from django.urls import path
from . import views

app_name = 'maps'

urlpatterns = [
    path('pp/', views.pp, name='pp'),
    path('datasets/', views.datasets, name='datasets'),

    path('datasets-unit-rumah/<str:kategori>/', views.maps_unit_rumah, name='maps-unit-rumah-by-kategori'),
    path('detail-json-unit-rumah/<int:pk>/', views.map_detail_json_unit_rumah, name='map-detail-json-unit-rumah'),

    path('datasets/<str:kategori>/', views.maps, name='maps-by-kategori'),
    path('detail-json/<int:pk>/', views.map_detail_json, name='map-detail-json'),

    path('datasets-object-add-rumah/<int:pk>/', views.maps_object_add_rumah, name='maps-object-add-rumah'),
    path('detail-json-object-add-rumah/<int:pk>/', views.maps_object_add_rumah_detail_json, name='map-object-add-rumah-detail-json'),
    path('datasets-object-update-rumah/<int:pk>/', views.maps_object_update_rumah, name='maps-object-update-rumah'),
    path('detail-json-object-update-rumah/<int:pk>/', views.maps_object_update_rumah_detail_json, name='map-object-udpate-rumah-detail-json'),

    path('datasets/add-map/', views.addMap, name='add-map'),

    path('datasets/delete-map/<str:kategori>/', views.deleteMaps, name='delete-maps'),

    path('check-progress/<str:task_id>/', views.check_progress, name='check_progress'),

    path('garis-pantai/', views.garis_pantai_view, name='garis-pantai'),
    path('kawasan-kumuh/', views.kawasan_kumuh_view, name='kawasan-kumuh'),
    path('jalan-lingkungan/', views.jalan_lingkungan_view, name='jalan-lingkungan'),
    path('rumah/', views.rumah_view, name='rumah'),

    path('peta-geojson/', views.peta_geojson, name='peta-geojson'),
    path("upload/", views.upload_geojson, name="upload-geojson"),
    path("upload-unit-rumah/", views.upload_geojson_unit_rumah, name="upload-unit-rumah-geojson"),

]
