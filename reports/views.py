from django.shortcuts import render
from journal.models import Transaction,Item
from catalogue.models import Account,Balance_type
from django.db.models import Q
from stateOfResult.models import Formula
from .templatetags.filters import getReservaLegal,getUtilidadDelEjercicio

def majorJournal(request):
    """
        Metodo que carga el reporte de libro mayor
    """
    principalAccounts = cuentaToMayorizar()
    mayor = calculoMayor(principalAccounts)
    journal = Transaction.objects.all()

    context = {
        'pricipalesCuentas' : principalAccounts,
        'detalleMayor' : mayor,
    }
    
    return render(request, 'reports/ledger.html', context)

def chekingBalance(request):
    """
        Metodo que carga el reporte de balanza de comprobacion
    """
    context = {
        'datos':calculoBalanza(),
        'total':sumaBalanza()
    }
    return render(request,'reports/balanceComprobación.html',context)

def balanceGenereal(request):

    suma_activo = sum(c['saldo'] for c in balanceGeneral() if c['cuenta'].name == 'ACTIVO')
    suma_pasivo = sum(c['saldo'] for c in balanceGeneral() if c['cuenta'].name == 'PASIVO')
    activoMasPasivo = suma_activo+suma_pasivo

    context = {
        'detalleBalance':balanceGeneral(),
        'suma': activoMasPasivo,

    }
    return render(request, "reports/balanceGeneral.html",context)

def catalogo(request):
    padres = Account.objects.filter(parent__isnull=True)
    cuentas = Account.objects.filter(parent__isnull=False)
    context = {
        'padres':padres,
        'cuentas':cuentas
    }
    return render(request,"reports/catalogo.html",context)

def libroDiario(request):

    context = {
        'partida':numberItemDiario(),
        'transacciones': Transaction.objects.all()
    }

    return render(request,'reports/libroDiario.html',context)

def cuentaToMayorizar():
    """
        Metodo que regreza las partidas de mayor que cuenten con alguna iteracion en el diario
    """
    principalAccounts = Account.objects.filter(parent__parent__isnull=False, parent__parent__parent__isnull=True)
    accountTransaccion = Transaction.objects.all()

    cuentaMostrar = []

    for p in principalAccounts:
        for t in accountTransaccion:
            if p.id == t.account.id or p.id == t.account.parent.id or p.id == t.account.parent.parent.id:
                cuentaMostrar.append(p)
                break  

    return cuentaMostrar

def getSaldo(j,type):
    """
        Calcula la el signo del balance para su suma
    """
    if type:
        if j.debit_credit:
            return -1*j.balance
        else:
            return j.balance
    else:
        if j.debit_credit:
            return j.balance
        else:
            return -1*j.balance
        
def numberItem():
    """
        Retorna el numero de partida + partida a la que pertenece
    """
    numero = []
    all_items = Item.objects.all().order_by('date')
    for index, item in enumerate(all_items, start=1):
        numero.append({'idItem': item.id, 'numero': index})
    return numero

def numberItemDiario():
    """
        Retorna el numero de partida + partida a la que pertenece
    """
    numero = []
    all_items = Item.objects.all().order_by('date')
    for index, item in enumerate(all_items, start=1):
        item.date = item.date.strftime('%Y-%m-%d')
        numero.append({'partida': item, 'numero': index})
    return numero

def calculoBalance(c,saldo):
    if c.account_r is False:
        return saldo
    else:
        return -1*saldo

def mayorCuenta(principalAccounts):
    """
        Retorna las cuentas mayorizadas, no se toma en cuenta las partidas de cierre
    """
    journal = Transaction.objects.all()
    cuentasMayorizadas = []
    for a in principalAccounts:
        contador = 0.0 
        try:
            tipo = Balance_type.objects.get(main_account=a.parent.parent)
        except Balance_type.DoesNotExist:
            tipo = None
        if tipo is not None:
            if not tipo.nature_of_balance:
                for j in journal:
                    if j.Item.isItemEnd is False:
                        if j.account.name == a.name or j.account.parent.name == a.name or j.account.parent.parent.name == a.name:
                            contador += getSaldo(j,True)                 
            else:
                for j in journal:
                    if j.Item.isItemEnd is False:
                        if j.account.name == a.name or j.account.parent.name == a.name or j.account.parent.parent.name == a.name:
                            contador += getSaldo(j,False)
            cuentasMayorizadas.append({'cuenta': a, 'saldo':contador})              
    return cuentasMayorizadas

def calculoMayor(principalAccounts):
    """
        Retorna las cuentas mayorizadas, toma en cuenta las partidas de cierre
    """
    journal = Transaction.objects.all()
    cuentasMayorizadas = []
    partida = numberItem()
    for a in principalAccounts:
        contador = 0.0 
        try:
            tipo = Balance_type.objects.get(main_account=a.parent.parent)
        except Balance_type.DoesNotExist:
            tipo = None
        if tipo is not None:
            if not tipo.nature_of_balance:
                for j in journal:
                    if j.account.id == a.id or j.account.parent.id == a.id or j.account.parent.parent.id == a.id:
                        contador += getSaldo(j,True)
                        num = 0
                        for p in partida:
                            if j.Item.id == p['idItem']:
                                num = p['numero']
                        cuentasMayorizadas.append({'main': a.name, 'transaccion':j, 'saldo':contador, 'numero':num})
            else:
                for j in journal:
                    if j.account.id == a.id or j.account.parent.id == a.id or j.account.parent.parent.id == a.id:
                        contador += getSaldo(j,False)
                        num = 0
                        for p in partida:
                            if j.Item.id == p['idItem']:
                                num = p['numero']
                        cuentasMayorizadas.append({'main': a.name, 'transaccion':j, 'saldo':round(contador,2), 'numero':num})              
    return cuentasMayorizadas


def calculoBalanza():
    """
     Retorna las cuentas con sus valores en el debe, haber, deudor y acreedor para la balanza de comprobacion
    """
    principalAccounts = cuentaToMayorizar()
    journal = Transaction.objects.all()
    cuentasBalance = []
    for a in principalAccounts:
        contador = 0.0 
        saldoDebe = 0.0
        saldoHaber = 0.0
        try:
            tipo = Balance_type.objects.get(main_account=a.parent.parent)
        except Balance_type.DoesNotExist:
            tipo = None 
        if tipo is not None:
            if not tipo.nature_of_balance:
                for j in journal:
                    if j.Item.isItemEnd is False:
                        if j.account.name == a.name or j.account.parent.name == a.name or j.account.parent.parent.name == a.name:
                            contador += getSaldo(j,True)
                            if(j.debit_credit is False):
                                saldoDebe += j.balance
                            else:
                                saldoHaber += j.balance
            else:
                for j in journal:
                    if j.Item.isItemEnd is False:
                        if j.account.name == a.name or j.account.parent.name == a.name or j.account.parent.parent.name == a.name:
                            contador += getSaldo(j,False)
                            if(j.debit_credit is False):
                                saldoDebe += j.balance
                            else:
                                saldoHaber += j.balance
            cuentasBalance.append({'main': a.name, 'saldo':round(contador,2), 'debe':round(saldoDebe,2), 'haber':round(saldoHaber,2), 'tipo':tipo.nature_of_balance})              
    return cuentasBalance

def sumaBalanza():
    """
        Devuelve totales para la balanza de comprobación
    """
    totalDebe = 0
    totalHaber = 0
    totalDeudor = 0
    totalAcreedor = 0
    for c in calculoBalanza():
        totalDebe += c['debe']
        totalHaber += c['haber']
        if c['tipo'] is False:
            totalDeudor += c['saldo']
        else:
            totalAcreedor += c['saldo']
    
    return {'tDebe':round(totalDebe,2),'tHaber':round(totalHaber,2),'tDeudor':round(totalDeudor,2),'tAcreedor':round(totalAcreedor,2)}

def balanceGeneral():
    """
        Devuelve array con partidas sumadas para mostrarse en el balance general
    """
    primaryAccounts = [Account.objects.get(name='ACTIVO'),Account.objects.get(name='PASIVO'),Account.objects.get(name='PATRIMONIO')]
    secondaryAccounts = Account.objects.filter(parent__isnull=False,parent__parent__isnull=True)
    tertaryAccounts = Account.objects.filter(parent__parent__isnull=False, parent__parent__parent__isnull=True)

    saldoInvFinal = Formula.objects.get(concept='Inventario Final')
    saldoReserva = getReservaLegal("a")
    saldoUtilidad = getUtilidadDelEjercicio("a")

    cuentasMayor = mayorCuenta(tertaryAccounts)
    cuentas = []
    for p in primaryAccounts:
        pCount = 0
        for s in secondaryAccounts:
            sCount = 0
            if s.parent.id == p.id:
                for t in cuentasMayor:
                    if t['cuenta'].parent.id == s.id:
                        if t['cuenta'].name == "INVENTARIOS":
                            t['saldo'] = saldoInvFinal.initial_value
                        if t['cuenta'].name == "UTILIDAD DEL EJERCICIO":
                            t['saldo'] = saldoUtilidad
                        if t['cuenta'].name == "RESERVA LEGAL":
                            t['saldo'] = saldoReserva  
                        sCount += calculoBalance(t['cuenta'],t['saldo'])
                        cuentas.append({'cuenta':t['cuenta'],'saldo':round(t['saldo'],2)})
                pCount += sCount
                cuentas.append({'cuenta':s,'saldo':round(sCount,2)})

        cuentas.append({'cuenta':p,'saldo':round(pCount,2)})

    return cuentas

