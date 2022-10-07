from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import LoginForm, RegisterForm
from .models import *


def home(request):
    return render(request, 'home.html')
 
 
def contact(request):
    return render(request, 'contact.html')
 
 
def loginUser(request):
    return render(request, 'accounts/registrations/login.html')


@transaction.atomic()
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.role = "ADMIN"
            user.save()
            current_site = get_current_site(request)
            subject = "Activate Your Account"
            message = render_to_string('accounts/registrations/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject=subject, message= message)
            return HttpResponse("Registered Successfully and Activation Sent")
    else:
        form = RegisterForm()
    return render(request,'accounts/registrations/register.html',{'form':form})


@transaction.atomic()
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        print(user.role)
        if user.role == "ADMIN":
            login(request,user)
            return redirect('accounts:admin_home')
        elif user.role == "STUDENT":
            login(request,user)
            
            return redirect('accounts:students_home')
        else:
            login(request,user)
            print(user.role)
            return redirect('accounts:staffs_home')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_active:
                    if "mfa" in settings.INSTALLED_APPS:
                        from mfa.helpers import has_mfa
                        res =  has_mfa(request,username=username)
                        if res:
                            return res
                        return login_user_in(request, username)
                else:
                    err="This student is NOT activated yet."
            else:
                context = {"error":"Wrong username and wrong password"}
                return render(request,'accounts/registrations/login.html',context)           



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

