# run_django.py
import os
import sys
from django.core.management import execute_from_command_line
from django.core.management import call_command

# Set lingkungan Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geoportal_perkimtan.settings')

# Inisialisasi Django
import django
django.setup()

# Periksa apakah aplikasi berjalan sebagai EXE
if not getattr(sys, 'frozen', False):
    # Jika bukan EXE, kumpulkan file statis
    call_command('collectstatic', '--noinput')

# Jalankan server
execute_from_command_line([sys.argv[0], 'runserver', '127.0.0.1:8000', '--noreload'])
