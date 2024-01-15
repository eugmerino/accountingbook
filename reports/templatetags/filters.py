from django import template

from journal.models import Transaction
from catalogue.models import Account,Balance_type
from stateOfResult.models import Formula, Term

register = template.Library()
saldo = 0
accountActual = None

@register.filter(name='get_calculated_balance')
def get_calculated_balance(account, transaccion):
    global saldo, accountActual
    if(accountActual!=account or accountActual==None):
        accountActual = account
        saldo = 0
    obj = Balance_type.objects.all().filter(main_account=account.parent.parent).first()
    if(obj.nature_of_balance):
        if transaccion.debit_credit:
            saldo += transaccion.balance
        else:
            saldo -= transaccion.balance
    else:
        if transaccion.debit_credit:
            saldo -= transaccion.balance
        else:
            saldo += transaccion.balance
    return saldo

@register.filter(name='mayorizar')
def mayorizar(account):
    debe = 0.00
    haber = 0.00
    listTransactions = Transaction.objects.all()
    obj = Balance_type.objects.all().filter(main_account=account.parent.parent).first()
    for trans in listTransactions:
        if not trans.Item.isItemEnd:
            if isDaughter(account, trans.account):
                if trans.debit_credit:
                    haber += trans.balance
                else:
                    debe += trans.balance
    if(obj.nature_of_balance):
        return round((haber-debe), 2)
    return round((debe-haber), 2)

def isDaughter(accountFather, accountDaughter):
    puntero = accountDaughter
    while puntero is not None and puntero.id != accountFather.id:
        puntero = puntero.parent
    if puntero is not None:
        return True
    return False

@register.filter(name='getTotalConcept')
def getTotalConcept(formula):
    totalConcept = 0.00
    if formula.initial_value != None:
        totalConcept = formula.initial_value
    listTerms = Term.objects.all()
    for term in listTerms:
        if(term.formula.id == formula.id):
            termValue = mayorizar(term.account)
            if term.operation:
                totalConcept += termValue
            else:
                totalConcept -= termValue
    return round(totalConcept, 2)

@register.filter(name='getComprasNetas')
def getComprasNetas(Parametro):
    comprasTotales = None
    comprasNetas = None
    listFromulas = Formula.objects.all()
    for formula in listFromulas:
        if formula.concept == "Compras Totales":
            comprasTotales = formula
        if formula.concept == "Compras Netas":
            comprasNetas = formula
    return round(getTotalConcept(comprasTotales) - getTotalConcept(comprasNetas), 2)

@register.filter(name='getMercaderiaDisponible')
def getMercaderiaDisponible(Parametro):
    mercaderiaDisponble = None
    listFromulas = Formula.objects.all()
    for formula in listFromulas:
        if formula.concept == "Mercadería Disponible Para la Venta":
            mercaderiaDisponble = formula
    return round(getComprasNetas("") + getTotalConcept(mercaderiaDisponble), 2)

@register.filter(name='getCostoDeVenta')
def getCostoDeVenta(Parametro):
    inventarioFinal = None
    listFromulas = Formula.objects.all()
    for formula in listFromulas:
        if formula.concept == "Inventario Final":
            inventarioFinal = formula
    return round(getMercaderiaDisponible("") - getTotalConcept(inventarioFinal), 2)

@register.filter(name='getUtilidadBruta')
def getUtilidadBruta(Parametro):
    ventasNetas = None
    listFromulas = Formula.objects.all()
    for formula in listFromulas:
        if formula.concept == "Ventas Netas":
            ventasNetas = formula
    return round(getTotalConcept(ventasNetas) - getCostoDeVenta(""), 2)

@register.filter(name='getGastosDeOperacion')
def getGastosDeOperacion(Parametro):
    gastosDeAdmin = None
    gastosDeVenta = None
    gastosFinancieros= None
    listFromulas = Formula.objects.all()
    for formula in listFromulas:
        if formula.concept == "Gastos de Administración":
            gastosDeAdmin = formula
        if formula.concept == "Gastos de Venta":
            gastosDeVenta = formula
        if formula.concept == "Gastos Financieros":
            gastosFinancieros = formula

    return round(getTotalConcept(gastosDeAdmin)+getTotalConcept(gastosDeVenta)+getTotalConcept(gastosFinancieros), 2)

@register.filter(name='getUtilidadDeOperacion')
def getUtilidadDeOperacion(Parametro):
    return round(getUtilidadBruta("")-getGastosDeOperacion(""), 2)

@register.filter(name='getUtilidadAntesReserva')
def getUtilidadAntesReserva(Parametro):
    otrosProductos = None
    otrosGastos = None
    listFromulas = Formula.objects.all()
    for formula in listFromulas:
        if formula.concept == "Otros Productos":
            otrosProductos = formula
        if formula.concept == "Otros Gastos":
            otrosGastos = formula
    return round(getUtilidadDeOperacion("")+getTotalConcept(otrosProductos)-getTotalConcept(otrosGastos), 2)

@register.filter(name='getReservaLegal')
def getReservaLegal(Parametro):
    return round(getUtilidadAntesReserva("")*0.07, 2)

@register.filter(name='getUtilidadAntesImpuesto')
def getUtilidadAntesImpuesto(Parametro):
    return round(getUtilidadAntesReserva("")-getReservaLegal(""), 2)

@register.filter(name='getImpuestoSobrelaRenta')
def getImpuestoSobrelaRenta(Parametro):
    utilidadAntesImpuesto = getUtilidadAntesImpuesto("")
    return round(utilidadAntesImpuesto*0.25 if utilidadAntesImpuesto<150000 else utilidadAntesImpuesto*0.30 , 2)

@register.filter(name='getUtilidadDelEjercicio')
def getUtilidadDelEjercicio(Parametro):
    return round(getUtilidadAntesImpuesto("")-getImpuestoSobrelaRenta(""), 2)