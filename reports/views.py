from django.shortcuts import render
from journal.models import Transaction, Item
from catalogue.models import Account, Balance_type
from django.db.models import Q
from stateOfResult.models import Formula
from django.db.models import Sum
from .templatetags.filters import get_utilidad_ejercicio,get_impuestoR,get_reserva_legal

def get_main_account(account):
    """
    devuelve la cuenta padre de una cuenta
    """
    while account.parent:
        account = account.parent
    return account

def get_descendants(account):
    """
    Devuelve una lista con las cuentas de su descendencia e incluida ella misma.
    """
    descendants = [account]  # Incluye la cuenta actual
    children = Account.objects.filter(parent=account)  # Busca los hijos directos
    for child in children:
        descendants.extend(get_descendants(child))  # Llama recursivamente para cada hijo
    return descendants

def account_balance(account):
    """
    Devuelve el saldo de una cuenta
    """
    descendants = get_descendants(account)
    transactions = Transaction.objects.filter(account__in=descendants)

    balanceType = Balance_type.objects.filter(main_account=get_main_account(account)).first()
    if not balanceType:
        return 0

    credit_sum = transactions.filter(debit_credit=True).aggregate(Sum('balance'))['balance__sum'] or 0
    debit_sum = transactions.filter(debit_credit=False).aggregate(Sum('balance'))['balance__sum'] or 0

    if balanceType.nature_of_balance:
        # Acreedor
        return credit_sum - debit_sum
    else:
        # Deudor
        return debit_sum - credit_sum

def transaction_details(account):
    """
    Devuelve los detalles de transacciones, incluyendo el saldo acumulativo.
    """
    descendants = get_descendants(account)
    transactions = Transaction.objects.filter(account__in=descendants).order_by('Item__date', 'id')  # Ordenar por fecha e ID
    items = Item.objects.all().order_by('date')

    # Crear un diccionario de número de partida
    item_numbers = {item.id: idx + 1 for idx, item in enumerate(items)}

    # Inicializar el saldo acumulado
    balanceType = Balance_type.objects.filter(main_account=get_main_account(account)).first()
    balance_nature = balanceType.nature_of_balance if balanceType else True  # Predeterminado a acreedor
    running_balance = 0

    # Construir los detalles de las transacciones
    details = []
    for transaction in transactions:
        balance = transaction.balance or 0

        # Actualizar el saldo acumulativo
        if transaction.debit_credit:
            # Si es crédito
            running_balance += balance if balance_nature else -balance
        else:
            # Si es débito
            running_balance -= balance if balance_nature else -balance

        # Obtener el número de partida
        item = transaction.Item
        item_number = item_numbers.get(item.id, None) if item else None

        # Agregar los detalles al diccionario
        details.append({
            'transaction': transaction,
            'item': item,
            'item_number': item_number,
            'running_balance': running_balance,  # Saldo acumulado
        })

    return details

def ledgerView(request):
    accounts = Transaction.objects.values_list('account', flat=True).distinct()
    print(f"Accounts encontrados: {list(accounts)}")
    ledger = [
        {'account': account, 'balance': account_balance(account), 'details': transaction_details(account)}
        for account in Account.objects.filter(pk__in=accounts)
    ]
    return render(request, 'reports/ledgerM.html', {'ledger': ledger})


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

    suma_activo = sum(c['saldo'] for c in balanceGeneral() if c['cuenta'].name == 'PATRIMONIO')
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
    saldoReserva = get_reserva_legal("a")
    saldoUtilidad = get_utilidad_ejercicio("a")
    saldoImpuestosPorPagar = get_impuestoR("a")
    print(saldoInvFinal.initial_value)
    print(saldoUtilidad)
    print(saldoImpuestosPorPagar)
    print(saldoReserva)

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
                        if t['cuenta'].name == "IMPUESTOS POR PAGAR":
                            t['saldo'] = saldoImpuestosPorPagar 
                        sCount += calculoBalance(t['cuenta'],t['saldo'])
                        cuentas.append({'cuenta':t['cuenta'],'saldo':round(t['saldo'],2)})
                pCount += sCount
                cuentas.append({'cuenta':s,'saldo':round(sCount,2)})

        cuentas.append({'cuenta':p,'saldo':round(pCount,2)})

    return cuentas

def cierreEjercicio(request):
    cierre = Item.objects.filter(isItemEnd = True)
    transacciones = Transaction.objects.filter(Item__isItemEnd = True)


    return render(request,'reports/cierre.html',{"cierre":cierre,"transaction":transacciones})