from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, UserForm, CustomPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

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

class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'forms.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Profile'
        context['subjudul'] = 'Profile'
        context['button'] = 'Save'
        context['post_form'] = self.get_form()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Your profile was successfully updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'forms.html'
    success_url = reverse_lazy('password-change')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Change Password'
        context['subjudul'] = 'Change Password'
        context['button'] = 'Save'
        context['post_form'] = self.get_form()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully changed!')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)