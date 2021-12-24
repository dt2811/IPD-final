from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import CreateUserForm

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'health/main.html', context)

# def update_user_data(user):
#     Profile.objects.update_or_create(user=user, defaults={'mob': user.profile.mob,})

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                # save = form.save()
                # save.refresh_from_db()
    
                # #newly added
                # save.profile.mob = form.cleaned_data.get('mob')
                # update_user_data(save) 
                
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                
                return redirect('login')
            
            
        context = {'form' : form}
        return render(request, 'health/register1.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else: 
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
        
            user = authenticate(request, username = username, password = password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or Password is incorrect")
            
        context = {}
        return render(request, 'health/login1.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def audvid(request):
    context = {}
    return render(request, 'health/audioorvideo.html', context)

@login_required(login_url='login')
def audio(request):
    context = {}
    return render(request, 'health/audio.html', context)

@login_required(login_url='login')
def video(request):
    context = {}
    return render(request, 'health/video.html', context)

