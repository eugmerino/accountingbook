from django import template

from journal.models import Transaction
from catalogue.models import Account,Balance_type
from stateOfResult.models import Formula, Term

register = template.Library()
saldo = 0
accountActual = None

ventasNetas = 0.00
comprasTotales = 0.00
comprasNetas = 0.00
mercaderiaDisponible = 0.00
inventarioFinal = 0.00
costoDeLoVendido = 0.00
utilidadBruta = 0.00
gastosAdmin = 0.00
gastosVentas = 0.00
gastosFinancieros = 0.00
gastosOperativos = 0.00
utilidadOperacion = 0.00
otrosProductos = 0.00
otrosGastos = 0.00
utilidadReserva = 0.00
reserva = 0.00
utilidadImpuesto = 0.00
impuestoR = 0.00
utilidadEjercicio = 0.00


@register.filter(name='get_concept_balance')
def get_concept_balance(concept, balance):
    global ventasNetas, comprasTotales, comprasNetas, mercaderiaDisponible, inventarioFinal, gastosAdmin, gastosVentas, gastosFinancieros, otrosProductos, otrosGastos, utilidadAntesReserva
    if concept == "Ventas Netas":
        ventasNetas = balance
    if concept == "Compras Totales":
        comprasTotales = balance
    if concept == "Compras Netas":
        balance += comprasTotales
        comprasNetas = balance
    if concept == "Mercadería Disponible Para la Venta":
        balance += comprasNetas
        mercaderiaDisponible = balance
    if concept == "Inventario Final":
        inventarioFinal = balance
    if concept == "Gastos de Administración":
        gastosAdmin = balance
    if concept == "Gastos de Venta":
        gastosVentas = balance
    if concept == "Gastos Financieros":
        gastosFinancieros = balance
    if concept == "Otros Productos":
        otrosProductos = balance
    if concept == "Otros Gastos":
        otrosGastos = balance

    return balance

@register.filter(name='get_costo_de_lo_vendido')
def get_costo_de_lo_vendido(value):
    global mercaderiaDisponible, inventarioFinal, costoDeLoVendido
    costoDeLoVendido = mercaderiaDisponible - inventarioFinal
    return costoDeLoVendido

@register.filter(name='get_utilidad_bruta')
def get_utilidad_bruta(value):
    global ventasNetas, costoDeLoVendido, utilidadBruta
    utilidadBruta = ventasNetas - costoDeLoVendido
    return round(utilidadBruta, 2)

@register.filter(name='get_gastos_operativos')
def get_gastos_operativos(value):
    global gastosOperativos, gastosAdmin, gastosVentas, gastosFinancieros
    gastosOperativos = gastosAdmin + gastosVentas + gastosFinancieros
    return round(gastosOperativos, 2)

@register.filter(name='get_utilidad_operacion')
def get_utilidad_operacion(value):
    global utilidadOperacion, gastosOperativos, utilidadBruta
    utilidadOperacion = utilidadBruta - gastosOperativos
    return round(utilidadOperacion, 2)

@register.filter(name='get_utilidad_reserva')
def get_utilidad_reserva(value):
    global utilidadOperacion, utilidadReserva, otrosProductos, otrosGastos
    utilidadReserva = utilidadOperacion + otrosProductos - otrosGastos
    return round(utilidadReserva, 2)

@register.filter(name='get_reserva_legal')
def get_reserva_legal(value):
    global utilidadReserva, reserva
    reserva = utilidadReserva*.07
    return round(reserva, 2)

@register.filter(name='get_utilidad_impuesto')
def get_utilidad_impuesto(value):
    global utilidadReserva, reserva, utilidadImpuesto
    utilidadImpuesto = utilidadReserva - reserva
    return round(utilidadImpuesto, 2)

@register.filter(name='get_impuestoR')
def get_impuestoR(value):
    global utilidadImpuesto, impuestoR
    if utilidadImpuesto <= 150000:
        impuestoR = utilidadImpuesto*0.25
    else:
        impuestoR = utilidadImpuesto*0.30
    return round(impuestoR, 2)

@register.filter(name='get_utilidad_ejercicio')
def get_utilidad_ejercicio(value):
    global utilidadImpuesto, impuestoR, utilidadEjercicio
    utilidadEjercicio = utilidadImpuesto - impuestoR
    return round(utilidadEjercicio, 2)


"""
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
"""