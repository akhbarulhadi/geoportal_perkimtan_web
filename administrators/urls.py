from django.urls import path
from . import views, views_permukiman, views_pengajuan, views_activity

app_name = 'administrators'

urlpatterns = [
    path('', views.index, name='index'),
    path('pp/', views_permukiman.pp, name='pp'),
    path('activity/', views_activity.activity, name='activity'),
    path('pengajuan/', views_pengajuan.pengajuan, name='pengajuan'),

    path('pp/unit-rumah/', views_permukiman.unitRumah, name='unit-rumah'),
    path('pp/data-rumah-belum-lengkap/', views_permukiman.dataRumahBelumLengkap, name='data-rumah-belum-lengkap'),
    path('pp/rlh', views_permukiman.RLH, name='rlh'),
    path('pp/rtlh', views_permukiman.RTLH, name='rtlh'),
    path('pp/rsewa', views_permukiman.rumahSewa, name='rsewa'),
    path('pp/rsubsidi', views_permukiman.rumahSubsidi, name='rsubsidi'),

    path('pp/perumahan', views_permukiman.perumahan, name='perumahan'),
    path('pp/psubsidi', views_permukiman.perumahanSubsidi, name='psubsidi'),
    path('pp/rusun', views_permukiman.rumahSusun, name='rusun'),

    path('pp/add-rumah/', views_permukiman.addRumah, name='add-rumah'),
    path('pp/add-rusun/', views_permukiman.addRusun, name='add-rusun'),

    path('pp/unit-rumah/add-perumahan/', views_permukiman.addPerumahan, name='add-perumahan'),
    path('pp/unit-rumah/popup-add-perumahan/', views_permukiman.addPerumahanPopUp, name='popup-add-perumahan'),
    path('pp/unit-rumah/add-kelurahan/', views_permukiman.addKelurahan, name='add-kelurahan'),
    path('pp/unit-rumah/add-kecamatan/', views_permukiman.addKecamatan, name='add-kecamatan'),

    path('pp/update-rumah/<int:pk>/', views_permukiman.updateRumah, name='update-rumah'),
    path('pp/update-perumahan/<int:pk>/', views_permukiman.updatePerumahan, name='update-perumahan'),
    path('pp/update-rusun/<int:pk>/', views_permukiman.updateRusun, name='update-rusun'),

    path('pp/delete-rumah/<int:pk>/', views_permukiman.deleteRumah, name='delete-rumah'),
    path('pp/delete-perumahan/<int:pk>/', views_permukiman.deletePerumahan, name='delete-perumahan'),
    path('pp/delete-rusun/<int:pk>/', views_permukiman.deleteRusun, name='delete-rusun'),

    path('pp/unit-rumah/view-request-add-rumah/', views_pengajuan.viewAddRequestRumah, name='view-request-add-rumah'),
    path('pp/unit-rumah/view-request-add-rumah-ditolak/', views_pengajuan.viewAddRequestRumahDitolak, name='view-request-add-rumah-ditolak'),
    path('pp/unit-rumah/view-request-add-rumah-disetujui/', views_pengajuan.viewAddRequestRumahDisetujui, name='view-request-add-rumah-disetujui'),
    path('pp/unit-rumah/request-add-rumah/', views_pengajuan.addRequestRumah, name='request-add-rumah'),
    path('pp/unit-rumah/proses-add-request-rumah/<int:pk>/', views_pengajuan.prosesAddRequestRumah, name='proses-add-request-rumah'),

    path('pp/unit-rumah/view-request-update-rumah/', views_pengajuan.viewUpdateRequestRumah, name='view-request-update-rumah'),
    path('pp/unit-rumah/view-request-update-rumah-ditolak/', views_pengajuan.viewUpdateRequestRumahDitolak, name='view-request-update-rumah-ditolak'),
    path('pp/unit-rumah/view-request-update-rumah-disetujui/', views_pengajuan.viewUpdateRequestRumahDisetujui, name='view-request-update-rumah-disetujui'),
    path('pp/unit-rumah/request-update-rumah/<int:pk>/', views_pengajuan.updateRequestRumah, name='request-update-rumah'),
    path('pp/unit-rumah/proses-update-request-rumah/<int:pk>/', views_pengajuan.prosesUpdateRequestRumah, name='proses-update-request-rumah'),

    path('pp/unit-rumah/view-request-delete-rumah/', views_pengajuan.viewRequestDeleteRumah, name='view-request-delete-rumah'),
    path('pp/unit-rumah/proses-delete-request-rumah/<int:pk>/', views_pengajuan.prosesDeleteRequstRumah, name='proses-delete-request-rumah'),
    path('pp/unit-rumah/request-delete-rumah/<int:pk>/', views_pengajuan.requestDeleteRumah, name='request-delete-rumah'),

    path('unit-rumah/<int:pk>/preview-pdf/', views_permukiman.preview_data_rumah_pdf, name='preview-data-rumah-pdf'),

    ]

