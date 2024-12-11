from django.shortcuts import render
from stateOfResult.models import Formula,Term
from reports.views import account_balance

def getFormulaBalance(formula):
    total = 0.00
    if formula.initial_value != None:
        total = formula.initial_value
    for term in Term.objects.filter(formula=formula):
        if(term.formula.id == formula.id):
            termValue = account_balance(term.account)
            if term.operation:
                total += termValue
            else:
                total -= termValue
    return round(total, 2)

def getFormulasBalance():
    data = []
    for formula in Formula.objects.all().order_by('-id'):
        total = formula.initial_value if formula.initial_value is not None else 0.00
        list_terms = []
        
        for term in Term.objects.filter(formula=formula):
            term_value = account_balance(term.account)
            if term.operation:
                total += term_value
            else:
                total -= term_value
            
            # Agregar el término y su valor al diccionario de términos
            list_terms.append({
                'term': term,
                'termValue': term_value
            })
        
        # Agregar la fórmula con su concepto, balance y términos al diccionario principal
        data.append({
            'concept': formula.concept,
            'balance': total,
            'listTerms': list_terms
        })
    
    return data

"""def getResultCalculations(data):
    resultCalculations = []
    ventasNetas = 0.00
    
    for formula in data:
        if formula['concept'] == "Ventas Netas":
            ventasNetas = formula['balance']
        resultCalculations.append({
            'Ventas Netas': ventasNetas,
            
        })

    return resultCalculations"""


def stateOfResultView(request):

    return render(request, 'reports/stateOfResult.html', {'data': getFormulasBalance()})