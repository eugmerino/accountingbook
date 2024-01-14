from django.shortcuts import render
from journal.models import Transaction
from catalogue.models import Account,Balance_type


def general_ledger_report(request):

    principalAccounts = Account.objects.filter(parent__parent__isnull=False, parent__parent__parent__isnull=True)
    
    journal = Transaction.objects.all()

    saldoNaturaleza = Balance_type.objects.all()
    
    calculoMayor(principalAccounts, journal)

    context = {
        'informacion' : 'Este sera el reporte del libro mayor.',
        'pricipalesCuentas' : principalAccounts,
        'detallePatidas' : journal,
    }
    return render(request, 'reports/ledger.html', context)

def calculoMayor(principalAccounts,journal):
        mayorCuentas = []
        for a in principalAccounts:
              tipo  = Balance_type.objects.get(main_account=a.parent.parent) #Obetenemos el tipo que es True: Acreedo False: Deudor
              acumulador = 0
                    
        return mayorCuentas