from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .forms import SignUpForm

class SignUpView(View):
    @method_decorator(never_cache)
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    
    @method_decorator(never_cache)
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('board_list')
        return render(request, 'signup.html', {'form': form})

class LoginView(View):
    @method_decorator(never_cache)
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    
    @method_decorator(never_cache)
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('board_list')
        return render(request, 'login.html', {'form': form})

class LogoutView(View):
    @method_decorator(never_cache)
    def get(self, request):
        logout(request)
        return redirect('home')

class HomeView(TemplateView):
    template_name = 'home.html'
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)