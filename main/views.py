from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from . import forms



# Create your views here.
def signIn(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is not None:
            login(request,user)
            return redirect('dashboard')
            
        return render(request,'SignIn.html',{
            'form': forms.MyAuthenticationForm,
            'error': "Usuario o contraseña incorrecto"
        })
            
        
    return render(request,'SignIn.html',{
        'form': forms.MyAuthenticationForm
    })

def dashBoard(request):
    return render(request,'dashboard.html')

