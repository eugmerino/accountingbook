from django.shortcuts import render
from journal.models import Transaction
from catalogue.models import Account,Balance_type

def general_stateOfResult_report(request):
    context = {
        'informacion' : 'Este sera el reporte del estado de resultado!!!!.',
    }
    return render(request, 'reports/stateOfResult.html', context)