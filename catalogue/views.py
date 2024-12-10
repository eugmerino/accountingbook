from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from .models import Balance_type
from .forms import accntForm
from .forms import natureForm
from django.contrib import messages

# Create your views here.
@login_required(login_url="/login")
def accountView(request):
    accounts = Account.objects.all().order_by("code")

    return render(request,'accounts.html',{
        'accounts':accounts
    })

@login_required(login_url="/login")
def createAccntView(request):
    accntForm2=accntForm()

    if request.method == 'POST':
        accntForm2 = accntForm(request.POST)

        item = accntForm2.save()

        if accntForm2.is_valid():
            messages.success(request, "La cuenta se ha guardado exitosamente.")
            return redirect('accounts')  
        else:
            messages.error(request, "El error fue empezar la carrera.")

    objects1={"accntForm":accntForm2}
    return render(request,'formAccnt.html',objects1)

@login_required(login_url="/login")
def natureView(request):
    natures = Balance_type.objects.all().order_by("main_account")

    return render(request,'natures.html',{
        'natures':natures
    })

@login_required(login_url="/login")
def createNaturView(request):
    natureForm2=natureForm()

    if request.method == 'POST':
        natureForm2 = natureForm(request.POST)

        item2 = natureForm2.save()

        if natureForm2.is_valid():
            messages.success(request, "La cuenta se ha guardado exitosamente.")
            return redirect('natures')  
        else:
            messages.error(request, "El error fue empezar la carrera.")

    objects2={"natureForm":natureForm}
    return render(request,'formNatur.html',objects2)
