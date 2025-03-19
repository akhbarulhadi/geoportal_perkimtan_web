from django.urls import path
from . import views

app_name = 'maps'

urlpatterns = [
    path('', views.index, name='index'),
    path('garis-pantai/', views.garis_pantai_view, name='garis-pantai'),
    ]

