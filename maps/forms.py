from django import forms
from .models import Maps, DataMaps, FieldMaps, GeoDataset

class mapsForm(forms.ModelForm):
    class Meta:
        model = Maps
        fields = ['nama', 'photo_maps', 'nama']
        labels = {
            'nama': 'Nama Maps',
            'photo_maps': 'Photo Maps',
            # 'nama': 'Field',
		}
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'block',
            }),
            'photo_maps': forms.ClearableFileInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'photo_maps',
            }),
        }

class GeoJSONUploadForm(forms.Form):
    file = forms.FileField(
        label="Unggah File GeoJSON",
        widget=forms.ClearableFileInput(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            'accept': '.geojson,.json'
        })
    )
    kategori = forms.CharField(
        label="Nama Dataset",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'kategori-select',
        })
    )
    # nama_dataset = forms.CharField(
    #     label="Nama Dataset",
    #     max_length=100,
    #     required=False,
    #     widget=forms.TextInput(attrs={
    #         'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
    #         'placeholder': 'Contoh: Sebaran Rumah Liar'
    #     })
    # )

class GeoJSONUploadUnitRumahForm(forms.Form):
    file = forms.FileField(
        label="Unggah File GeoJSON Untuk Unit Rumah",
        widget=forms.ClearableFileInput(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            'accept': '.geojson,.json'
        })
    )
