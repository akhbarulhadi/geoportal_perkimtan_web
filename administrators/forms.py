from django import forms
from gis_data.models import Rumah, Kecamatan, Kelurahan, Perumahan

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
        model = Rumah
        fields = ['block', 'nama_perumahan', 'kelurahan', 'kecamatan', 'lokasi_rumah', 'status_rumah', 'rawan_bencana']
        labels = {
            'block': 'Block',
            'nama_perumahan': 'Nama Perumahan',
            'kelurahan': 'Kelurahan',
            'kecamatan': 'Kecamatan',
            'lokasi_rumah': 'Lokasi Rumah',
            'status_rumah': 'Status Rumah',
            'rawan_bencana': 'Apakah rumah ini rawan bencana ?',
		}
        widgets = {
            'block': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'block',
            }),
            'lokasi_rumah': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'lokasi_rumah',
            }),
            'status_rumah': forms.Select(attrs={
                'class': 'select2',
                'placeholder': '',
                'id': 'status_rumah',
            }),
            'rawan_bencana': forms.CheckboxInput(attrs={
                'class': 'checked:border-indigo-500 h-5 w-5',
                'placeholder': '',
                'id': 'rawan_bencana',
            }),
        }


class perumahanForm(forms.ModelForm):
    class Meta:
        model = Perumahan
        fields = ['nama_perumahan', 'lokasi_perumahan']
        labels = {
            'nama_perumahan': 'Nama Perumahan',
            'lokasi_perumahan': 'Lokasi Perumahan'
		}
        widgets = {
            'nama_perumahan': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'nama_perumahan',
            }),
            'lokasi_perumahan': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-cyan-600 focus:border-cyan-600 block w-full p-2.5',
                'placeholder': '',
                'id': 'lokasi_perumahan',
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