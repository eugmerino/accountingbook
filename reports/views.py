from django.shortcuts import render

def general_ledger_report(request):
    context = {
        'informacion': 'Este sera el reporte del libro mayor.',
    }
    return render(request, 'reports/ledger.html', context)