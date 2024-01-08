from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout,get_user
from django.contrib.auth.decorators import login_required
from . import forms



# Create your views here.
def start(request):
    if request.method == 'POST':
        return redirect('login')
    return render(request,'start.html')

def signIn(request):
    if request.method == 'POST':

        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request,user)
            return redirect('dashboard')
            
        return render(request,'login.html',{
            'form': forms.MyAuthenticationForm,
            'error': "Usuario o contraseña incorrecto"
        })
            
        
    return render(request,'login.html',{
        'form': forms.MyAuthenticationForm
    })

@login_required(login_url="login/")
def dashBoard(request):
    user = get_user(request)
    return render(request,'dashboard.html',{
        'user': user
    })

@login_required(login_url="login/")
def singOut(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request,'logout.html')


