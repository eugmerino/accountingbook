from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import accntForm
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

        if accntForm2.is_valid():
            
            item = accntForm2.save()

            messages.success(request, "La cuenta se ha guardado exitosamente.")
            return redirect('accounts')  
        else:
            messages.error(request, "El error fue empezar la carrera.")

    objects={"accntForm":accntForm2}
    return render(request,'formAccnt.html',objects)