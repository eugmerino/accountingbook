from django.shortcuts import render
from stateOfResult.models import Formula,Term

def stateOfResultView(request):

    listFormulas = Formula.objects.all().order_by('-id')
    listTerms = Term.objects.all()
    context = {
        'listFormulas': listFormulas,
        'listTerms': listTerms,
    }
    return render(request, 'reports/stateOfResult.html', context)