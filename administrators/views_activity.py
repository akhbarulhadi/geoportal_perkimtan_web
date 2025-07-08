from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry

@login_required(login_url='/login')
def activity(request):
    permission_admin = ['admin',]
    admin = request.user.groups.filter(name__in=permission_admin).exists()
    permission_operator = ['operator',]
    operator = request.user.groups.filter(name__in=permission_operator).exists()

    recent_actions = LogEntry.objects.filter(user=request.user).select_related('user', 'content_type').order_by('-action_time')[:20]

    isi = {
		    'page_title': 'Aktivitas Pengguna',
		    'subjudul': 'Aktivitas Pengguna',
        'recent_actions': recent_actions,
        'admin': admin,
        'operator': operator,
    }
    return render(request,'administrators/activity.html', isi)
