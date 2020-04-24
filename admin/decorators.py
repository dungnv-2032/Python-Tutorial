from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse


def admin_required(function):

    def wrapper(request, *args, **kwargs):

        if request.user is not None and request.user.is_superuser != 1 :
            messages.error(request, 'Permission Denied !')

            return redirect(reverse('admin:admin-login'))

        return function(request, *args, **kwargs)

    return wrapper
