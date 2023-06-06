from django.shortcuts import redirect, render
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created! You are now able to log in")
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'pages/user/register.html' ,context)

@login_required
def profile(request):
    if request.method == 'POST':
        updateform = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if updateform.is_valid() and p_form.is_valid():
            updateform.save()
            p_form.save()
            messages.success(request, f'Your account has been update!')
            return redirect('profile')
    else:
        updateform = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'title' : 'register',
        'updateform': updateform,
        'p_form': p_form,
    }
    return render(request, 'pages/user/profile.html', context)

# @login_required(login_url='login')
# def userupdate(request, id):
    # updateprofile = User.objects.get(id=id)
    # if request.method == 'POST':
    #     updateprofile_save = UserUpdateForm(request.POST, instance=updateprofile)
    #     if updateprofile_save.is_valid():
    #         updateprofile_save.save()
    #         messages.success(request, f'I have updated your details!')
    #         return redirect('profile')
    # else:
    #     updateprofile_save = UserUpdateForm(request.POST, instance=updateprofile)

    # context = {
    #     'updateprofile' : updateprofile_save,
    # }

    # return render(request, 'pages/user/update.html', context)