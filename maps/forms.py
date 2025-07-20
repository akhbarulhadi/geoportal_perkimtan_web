from django import forms

class GeoJSONUploadForm(forms.Form):
    file = forms.FileField(
        label="Unggah File GeoJSON",
        widget=forms.ClearableFileInput(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
            'accept': '.geojson,.json'
        })
    )
    kategori = forms.CharField(
        label="Nama Map",
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
    nama_dataset = forms.CharField(
        label="Item Menu Untuk Filter",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'nama-dataset-select',
        })
    )
