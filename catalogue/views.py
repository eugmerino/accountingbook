from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Account

# Create your views here.
@login_required(login_url="/login")
def accountView(request):
    accounts = Account.objects.all()

    return render(request,'accounts.html',{
        'accounts':accounts
    })