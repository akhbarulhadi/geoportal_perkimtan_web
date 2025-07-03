from django.urls import path
from . import views

app_name = 'administrators'

urlpatterns = [
    path('', views.index, name='index'),
    path('pp/', views.pp, name='pp'),
    path('activity/', views.activity, name='activity'),
    path('pengajuan/', views.pengajuan, name='pengajuan'),

    path('pp/unit-rumah/', views.unitRumah, name='unit-rumah'),
    # path('pp/unit-rumah/rumah-list/', views.rumah_list_view, name='rumah-list'),
    path('pp/rlh', views.RLH, name='rlh'),
    path('pp/rtlh', views.RTLH, name='rtlh'),
    path('pp/rsewa', views.rumahSewa, name='rsewa'),
    path('pp/rsubsidi', views.rumahSubsidi, name='rsubsidi'),

    path('pp/perumahan', views.perumahan, name='perumahan'),
    path('pp/psubsidi', views.perumahanSubsidi, name='psubsidi'),
    path('pp/rusun', views.rumahSusun, name='rusun'),

    path('pp/add-rumah/', views.addRumah, name='add-rumah'),
    path('pp/add-rusun/', views.addRusun, name='add-rusun'),

    path('pp/unit-rumah/add-perumahan/', views.addPerumahan, name='add-perumahan'),
    path('pp/unit-rumah/popup-add-perumahan/', views.addPerumahanPopUp, name='popup-add-perumahan'),
    path('pp/unit-rumah/add-kelurahan/', views.addKelurahan, name='add-kelurahan'),
    path('pp/unit-rumah/add-kecamatan/', views.addKecamatan, name='add-kecamatan'),

    path('pp/update-rumah/<int:pk>/', views.updateRumah, name='update-rumah'),
    path('pp/update-perumahan/<int:pk>/', views.updatePerumahan, name='update-perumahan'),
    path('pp/update-rusun/<int:pk>/', views.updateRusun, name='update-rusun'),

    path('pp/delete-rumah/<int:pk>/', views.deleteRumah, name='delete-rumah'),
    path('pp/delete-perumahan/<int:pk>/', views.deletePerumahan, name='delete-perumahan'),
    path('pp/delete-rusun/<int:pk>/', views.deleteRusun, name='delete-rusun'),

    path('activity/', views.activity_summary, name='activity'),

    path('pp/unit-rumah/view-request-add-rumah/', views.viewAddRequestRumah, name='view-request-add-rumah'),
    path('pp/unit-rumah/view-request-add-rumah-ditolak/', views.viewAddRequestRumahDitolak, name='view-request-add-rumah-ditolak'),
    path('pp/unit-rumah/view-request-update-rumah/', views.viewUpdateRequestRumah, name='view-request-update-rumah'),
    path('pp/unit-rumah/request-update-rumah/<int:pk>/', views.updateRequestRumah, name='request-update-rumah'),
    path('pp/unit-rumah/request-add-rumah/', views.addRequestRumah, name='request-add-rumah'),
    path('pp/unit-rumah/proses-request-rumah/<int:pk>/', views.prosesRequestRumah, name='proses-request'),

    ]

