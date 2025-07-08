from django import forms
from gis_data.models import Rumah, Kecamatan, Kelurahan, Perumahan, RumahSusun, AddRequest
# from leaflet.forms.widgets import LeafletWidget
from django.contrib.gis import forms as geo_forms
from maps.models import GeoDataset


class geoForm(forms.ModelForm):
    class Meta:
        model = GeoDataset
        fields = ['geometry']
        labels = {
            'geometry': 'Koordinat Rumah',
		}
        widgets = {
            'geometry': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'geometry',
                'add_map_geo_button': True,
                'readonly': 'readonly',
            }),
        }

class rumahForm(forms.ModelForm):
    nama_perumahan = forms.ModelChoiceField(
        queryset=Perumahan.objects.all(),
        label="Nama Perumahan",
        widget=forms.Select(attrs={
            'class': 'select2',
            'id': 'nama_perumahan',
            'addable': True,
        })
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nama_perumahan'].label_from_instance = lambda obj: f"{obj.nama_perumahan}  ({obj.kelurahan} - {obj.kecamatan})"

    class Meta:
        model = Rumah
        fields = ['photo_rumah', 'nama_pemilik', 'alamat_rumah', 'jumlah_kk', 'nilai_keselamatan', 'nilai_kesehatan', 'nilai_komponen', 'nama_perumahan', 'status_rumah', 'status_luas', 'rumah_sewa', 'dibuat_oleh_users']
        labels = {
            'photo_rumah': 'Photo Rumah',
            'nama_pemilik': 'Nama Pemilik',
            'alamat_rumah': 'Alamat Rumah',
            'jumlah_kk': 'Jumlah KK',
            'nilai_keselamatan': 'Nilai Keselamatan',
            'nilai_kesehatan': 'Nilai Kesehatan',
            'nilai_komponen': 'Nilai Komponen & Bahan Bangunan',
            'nama_perumahan': 'Nama Perumahan',
            'status_rumah': 'Status Rumah',
            'status_luas': 'Status Luas',
            'rumah_sewa': 'Apakah Ini Rumah Sewa?',
            'dibuat_oleh_users': 'Email Pemilik',
		}
        widgets = {
            'photo_rumah': forms.ClearableFileInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'photo_rumah',
            }),
            'nama_pemilik': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'nama_pemilik',
            }),
            'alamat_rumah': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'alamat_rumah',
            }),
            'jumlah_kk': forms.NumberInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'jumlah_kk',
            }),
            'nilai_keselamatan': forms.NumberInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'nilai_keselamatan',
            }),
            'nilai_kesehatan': forms.NumberInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'nilai_kesehatan',
            }),
            'nilai_komponen': forms.NumberInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'nilai_komponen',
            }),
            'status_rumah': forms.Select(attrs={
                'class': 'select2',
                'placeholder': '',
                'id': 'status_rumah',
            }),
            'status_luas': forms.Select(attrs={
                'class': 'select2',
                'placeholder': '',
                'id': 'status_luas',
            }),
            'rumah_sewa': forms.CheckboxInput(attrs={
                'class': 'checked:border-indigo-500 h-5 w-5',
                'placeholder': '',
                'id': 'rumah_sewa',
            }),
            'dibuat_oleh_users': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'dibuat_oleh_users',
            }),
            # 'lokasi_rumah': forms.TextInput(attrs={
            #     'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            #     'placeholder': '',
            #     'id': 'lokasi_rumah',
            #     'disabled': 'disabled',
            #     # 'readonly': 'readonly',
            # }),
            # 'lokasi_rumah': forms.TextInput(attrs={
            #     'id': 'id_titik',
            #     'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            #     'placeholder': '',
            #     'readonly': 'readonly',
            #     'add_map_button': True,
            #     }),
            # 'lokasi_rumah': geo_forms.OSMWidget(attrs={
            #     'map_width': 800,
            #     'map_height': 500,
            # }),
            # 'lokasi_rumah': LeafletWidget(attrs={
            #     'map_width': '100%',
            #     'map_height': '400px',
            #     'map_srid': 4326,
            #     'settings_overrides': {
            #         'DEFAULT_CENTER': (-6.2, 106.8),  # Koordinat Jakarta
            #         'DEFAULT_ZOOM': 12,
            #         'EDIT_CONTROL': True,
            #         'PLUGINS': {
            #             'forms': {
            #                 'auto': True,
            #                 'default': 'point',
            #                 'only': ['point', 'polygon', 'linestring'],
            #             },
            #             'draw': {
            #                 'polygon': {
            #                     'allowIntersection': False,
            #                     'showArea': True
            #                 }
            #             }
            #         }
            #     }
            # })
        }

class perumahanForm(forms.ModelForm):
    kelurahan = forms.ModelChoiceField(
        queryset=Kelurahan.objects.all(),
        label="Nama Kelurahan",
        widget=forms.Select(attrs={
            'class': 'select2',
            'id': 'kelurahan',
            'addable': True,
        })
    )
    kecamatan = forms.ModelChoiceField(
        queryset=Kecamatan.objects.all(),
        label="Nama Kecamatan",
        widget=forms.Select(attrs={
            'class': 'select2',
            'id': 'kecamatan',
            'addable': True,
        })
    )

    class Meta:
        model = Perumahan
        fields = ['nama_perumahan', 'photo_perumahan', 'kelurahan', 'kecamatan', 'alamat_lengkap_perumahan', 'perumahan_subsidi']
        labels = {
            'nama_perumahan': 'Nama Perumahan',
            'photo_perumahan': 'Foto Gerbang',
            'kelurahan': 'Kelurahan',
            'kecamatan': 'Kecamatan',
            'alamat_lengkap_perumahan': 'Alamat Lengkap Perumahan',
            # 'lokasi_perumahan': 'Koordinat Perumahan',
            'perumahan_subsidi': 'Apakah Perumahan ini subsidi ?'
		}
        widgets = {
            'nama_perumahan': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'nama_perumahan',
            }),
            'photo_perumahan': forms.ClearableFileInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'photo_perumahan',
            }),
            'alamat_lengkap_perumahan': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'alamat_lengkap_perumahan',
            }),
            # 'lokasi_perumahan': forms.TextInput(attrs={
            #     'id': 'id_titik',
            #     'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            #     'placeholder': '',
            #     'readonly': 'readonly',
            #     'add_map_button': True,
            # }),
            'perumahan_subsidi': forms.CheckboxInput(attrs={
                'class': 'checked:border-indigo-500 h-5 w-5',
                'placeholder': '',
                'id': 'perumahan_subsidi',
            })
        }

class kelurahanForm(forms.ModelForm):
    class Meta:
        model = Kelurahan
        fields = ['kelurahan']
        labels = {
            'kelurahan': 'Kelurahan',
		}
        widgets = {
            'kelurahan': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'nama_perumahan',
            })
        }

class kecamatanForm(forms.ModelForm):
    class Meta:
        model = Kecamatan
        fields = ['kecamatan']
        labels = {
            'kecamatan': 'Kecamatan',
		}
        widgets = {
            'kecamatan': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'nama_perumahan',
            })
        }

class rusunForm(forms.ModelForm):
    kelurahan = forms.ModelChoiceField(
        queryset=Kelurahan.objects.all(),
        label="Nama Kelurahan",
        widget=forms.Select(attrs={
            'class': 'select2',
            'id': 'kelurahan',
            'addable': True,
        })
    )
    kecamatan = forms.ModelChoiceField(
        queryset=Kecamatan.objects.all(),
        label="Nama Kecamatan",
        widget=forms.Select(attrs={
            'class': 'select2',
            'id': 'kecamatan',
            'addable': True,
        })
    )
    class Meta:
        model = RumahSusun
        fields = ['photo_rusun', 'nama_rusun', 'alamat_rusun', 'kelurahan', 'kecamatan', 'jumlah_kk', 'jumlah_unit_kamar', 'lokasi_rusun']
        labels = {
            'photo_rusun': 'Foto Rusun',
            'nama_rusun': 'Nama Rusun',
            'alamat_rusun': 'Alamat Rusun',
            'kelurahan': 'Kelurahan',
            'kecamatan': 'Kecamatan',
            'jumlah_kk': 'Jumlah KK',
            'jumlah_unit_kamar': 'Jumlah Unit Kamar',
            'lokasi_rusun': 'Koordinat Rusun',
		}
        widgets = {
            'photo_rusun': forms.ClearableFileInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'photo_rusun',
            }),
            'nama_rusun': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'nama_rusun',
            }),
            'alamat_rusun': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'alamat_rusun',
            }),
            'jumlah_kk': forms.NumberInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'jumlah_kk',
            }),
            'jumlah_unit_kamar': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'jumlah_unit_kamar',
            }),
            # 'lokasi_rusun': forms.TextInput(attrs={
            #     'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            #     'placeholder': '',
            #     'id': 'lokasi_rusun',
            #     'disabled': 'disabled',
            # }),
            'lokasi_rusun': forms.TextInput(attrs={
                'id': 'id_titik',
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'readonly': 'readonly',
                'add_map_button': True,
                }),
        }

class RumahAddRequestForm(forms.ModelForm):
    nama_pemilik = forms.CharField(
        label='Nama Pemilik',
        widget=forms.TextInput(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            'id': 'nama_pemilik',
        }))
    alamat_rumah = forms.CharField(
        label='Alamat Rumah',
        widget=forms.TextInput(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            'id': 'alamat_rumah',
        }))
    jumlah_kk = forms.IntegerField(
        label='Jumlah KK',
        widget=forms.NumberInput(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            'id': 'jumlah_kk',
        }))
    nilai_keselamatan = forms.IntegerField(
        label='Nilai Keselamatan',
        widget=forms.NumberInput(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            'id': 'nilai_keselamatan',
        }))
    nilai_kesehatan = forms.IntegerField(
        label='Nilai Kesehatan',
        widget=forms.NumberInput(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            'id': 'nilai_kesehatan',
        }))
    nilai_komponen = forms.IntegerField(
        label='Nilai Komponen',
        widget=forms.NumberInput(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            'id': 'nilai_komponen',
        }))
    nama_perumahan = forms.ModelChoiceField(
        queryset=Perumahan.objects.all(),
        label="Nama Perumahan",
        widget=forms.Select(attrs={
            'class': 'select2',
            'id': 'nama_perumahan',
            # 'addable': True,
        })
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nama_perumahan'].label_from_instance = lambda obj: f"{obj.nama_perumahan}  ({obj.kelurahan} - {obj.kecamatan})"
    status_rumah = forms.ChoiceField(
        label='Status Rumah',
        choices=Rumah.STATUS_RUMAH_CHOICES,
        widget=forms.Select(attrs={
            'class': 'select2',
            'id': 'status_rumah',
        }))
    status_luas = forms.ChoiceField(
        label='Status Luas',
        choices=Rumah.STATUS_LUAS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'select2',
            'id': 'status_luas',
        }))
    rumah_sewa = forms.BooleanField(
        required=False,
        label='Rumah Sewa',
        widget=forms.CheckboxInput(attrs={
            'class': 'checked:border-indigo-500 h-5 w-5',
            'id': 'rumah_sewa',
        }))

    class Meta:
        model = AddRequest
        fields = ['photo_rumah', 'nama_pemilik', 'alamat_rumah', 'jumlah_kk', 'nilai_keselamatan', 'nilai_kesehatan', 'nilai_komponen', 'nama_perumahan', 'status_rumah', 'status_luas', 'rumah_sewa', 'geometry']
        labels = {
            'photo_rumah': 'Foto Rumah',
            'geometry': 'Koordinat Rumah',
        }
        widgets = {
            'photo_rumah': forms.ClearableFileInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'photo_rumah',
            }),
            'geometry': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'geometry',
                'add_map_geo_button': True,
                'readonly': 'readonly',
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.data = {
            'nama_pemilik': self.cleaned_data['nama_pemilik'],
            'alamat_rumah': self.cleaned_data['alamat_rumah'],
            'jumlah_kk': self.cleaned_data['jumlah_kk'],
            'nilai_keselamatan': self.cleaned_data['nilai_keselamatan'],
            'nilai_kesehatan': self.cleaned_data['nilai_kesehatan'],
            'nilai_komponen': self.cleaned_data['nilai_komponen'],
            'nama_perumahan': str(self.cleaned_data['nama_perumahan']),
            'status_rumah': self.cleaned_data['status_rumah'],
            'status_luas': self.cleaned_data['status_luas'],
            'rumah_sewa': self.cleaned_data['rumah_sewa'],
        }

        if commit:
            instance.save()
        return instance

