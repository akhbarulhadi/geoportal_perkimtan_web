from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login')
def index(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    isi = {
		'page_title': 'Utama',
    'admin': admin,
    'operator': operator,
    }
    return render(request,'administrators/index.html', isi)

