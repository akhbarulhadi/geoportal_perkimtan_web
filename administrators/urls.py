from django.urls import path
from . import views

app_name = 'administrators'

urlpatterns = [
    path('', views.index, name='index'),
    path('pp/', views.pp, name='pp'),

    path('pp/unit-rumah/', views.unitRumah, name='unit-rumah'),
    path('pp/rlh', views.RLH, name='rlh'),
    path('pp/rtlh', views.RTLH, name='rtlh'),
    path('pp/dkb', views.rawanBencana, name='dkb'),

    path('pp/add-rumah/', views.addRumah, name='add-rumah'),

    path('pp/unit-rumah/add-perumahan/', views.addPerumahan, name='add-perumahan'),
    path('pp/unit-rumah/add-kelurahan/', views.addKelurahan, name='add-kelurahan'),
    path('pp/unit-rumah/add-kecamatan/', views.addKecamatan, name='add-kecamatan'),

    path('activity/', views.activity_summary, name='activity'),
    ]

