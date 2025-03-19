from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(request.user)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')

                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')

                context = {
                    'form': form,
                    'page_title': 'Login',
                    'button': 'Login',
                }
                return render(request, 'index.html', context)
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'page_title': 'Login',
        'button': 'Login',
    }
    return render(request, 'index.html', context)


def user_logout(request):
    logout(request)

    return redirect('login')