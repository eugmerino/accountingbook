from django.shortcuts import render
from journal.models import Transaction
from catalogue.models import Account,Balance_type


def general_ledger_report(request):

    principalAccounts = Account.objects.filter(parent__parent__isnull=False, parent__parent__parent__isnull=True)
    
    journal = Transaction.objects.all()

    context = {
        'informacion' : 'Este sera el reporte del libro mayor.',
        'pricipalesCuentas' : principalAccounts,
        'detallePatidas' : journal,
    }
    return render(request, 'reports/ledger.html', context)
