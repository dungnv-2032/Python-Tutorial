from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout


def admin_required(function):
    template_name = 'admin_login.html'

    def wrapper(request, *args, **kwargs):

        if request.user is not None and request.user.is_superuser != 1 :
            messages.error(request, 'Permission Denied !')
            return render(request, template_name)

        return function(request, *args, **kwargs)

    return wrapper
