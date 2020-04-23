from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.urls import reverse


def logout_view(request):
    logout(request)

    return redirect('user:login')


class LoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('book:index')
        return render(request, self.template_name)

    def post(self, request):
        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Username or Password Invalid')

        return HttpResponseRedirect('/login/')


class RegisterView(View):
    template_name = 'register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        register_form = self.form_class(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)

            return redirect('book:index')

        return render(request, self.template_name, {'form': register_form})
