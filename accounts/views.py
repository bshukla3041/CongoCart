from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from phonenumber_field.phonenumber import PhoneNumber
from django.contrib import messages

from .forms import RegistrationForm, PasswordSettingForm, LoginForm, UpdateProfileForm
from .models import CongoUser, CongoUserProfile


@csrf_protect
def register_view(request):
    template = 'accounts/register.html'
    context = {}
    if request.POST:
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            _phone_number = register_form.cleaned_data.get('phone_number')
            phone_number = _phone_number.as_national
            request.session['phone_number'] = phone_number
            return redirect('set-password')
        else:
            context['form'] = register_form
    else:
        register_form = RegistrationForm()
        context['form'] = register_form
    return render(request, template, context)


@csrf_protect
def password_set_view(request):
    template = 'accounts/password_set.html'
    context = {}
    if request.POST:
        password_form = PasswordSettingForm(request.POST)
        if password_form.is_valid():
            _phone_number = request.session['phone_number']
            phone_number = PhoneNumber.from_string(
                phone_number=_phone_number, region='IN').as_national
            password = password_form.cleaned_data.get('password1')
            congo_user = CongoUser.objects.create_user(
                phone_number=phone_number, password=password)
            login(request, congo_user)
            messages.success(request, 'Your account has been successfully setup. Welcome to CongoCart !')
            return redirect('home')
        else:
            context['form'] = password_form
    else:
        password_form = PasswordSettingForm()
        context['form'] = password_form
    return render(request, template, context)


def login_view(request):
    template = 'accounts/login.html'
    context = {}
    congo_user = request.user
    if congo_user.is_authenticated:
        return redirect('home')
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            phone_number = login_form.cleaned_data.get('phone_number')
            password = login_form.cleaned_data.get('password')
            congo_user = authenticate(
                request, phone_number=phone_number, password=password)
            login(request, congo_user)
            return redirect('home')
        else:
            print('Invalid login credentials')
            context['form'] = login_form
    else:
        login_form = LoginForm()
        context['form'] = login_form
    return render(request, template, context)


@login_required
def logout_view(request):
    template = 'accounts/logout.html'
    context = {}
    logout(request)
    return render(request, template, context)


@login_required
def update_profile_view(request):
    context = {}
    template = 'accounts/update_profile.html'
    update_profile_form = None
    congo_user = request.user
    congo_user_profile = CongoUserProfile.objects.filter(congo_user=congo_user)
    if congo_user_profile.count() > 0:
        congo_user_profile = congo_user_profile.first()
        update_profile_form = UpdateProfileForm(instance=congo_user_profile)
    if request.POST:
        update_profile_form = UpdateProfileForm(request.POST)
        if update_profile_form.is_valid():
            profile = update_profile_form.save(commit=False)
            profile.congo_user = request.user
            profile.is_verified = True
            profile.save()
            return redirect('home')
        else:
            context['form'] = update_profile_form
    else:
        if update_profile_form is None:
            update_profile_form = UpdateProfileForm()
        context['form'] = update_profile_form
    return render(request, template, context)
