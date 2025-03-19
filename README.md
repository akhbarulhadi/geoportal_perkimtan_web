# Django GIS Project

Ini adalah proyek Django dengan dukungan GIS menggunakan PostgreSQL dan PostGIS.

## 📌 Persyaratan
- Python 3.12
- Django 5.1.2
- PostgreSQL + PostGIS
- GDAL dan GEOS (dari OSGeo4W)
- Node.js (untuk Tailwind, opsional)

## 🚀 Instalasi

1. **Buat Virtual Environment & Aktifkan**
   ```sh
   python -m venv Env
   Env\Scripts\activate.bat     # Untuk Windows
   ```

2. **Clone Repository & Install Dependencies**
   ```sh
   git clone https://github.com/akhbarulhadi/geoportal_perkimtan_web.git
   cd geoportal_perkimtan_web
   pip install -r requirements.txt
   ```

3. **Jalankan Server**
   ```sh
   python manage.py runserver
   ```

## 📂 Struktur Folder
```
├── geoportal_perkimtan_web
│   ├── administrators
│   ├── gis_data
│   ├── maps
│   ├── static
│   ├── templates
│   ├── theme
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
```

## 🛠 Troubleshooting
- **Jika Peta Tidak Muncul di Admin**
  1. Cek apakah `django.contrib.gis` sudah ada di `INSTALLED_APPS`.
  2. Pastikan `GDAL_LIBRARY_PATH` dan `GEOS_LIBRARY_PATH` dikonfigurasi di `settings.py`.
  3. Pastikan koordinat dalam EPSG:4326.


