from django.shortcuts import render
from journal.models import Transaction,Item
from catalogue.models import Account,Balance_type
from django.db.models import Q

def cuentaToMayorizar():
    principalAccounts = Account.objects.filter(parent__parent__isnull=False, parent__parent__parent__isnull=True)
    accountTransaccion = Transaction.objects.all()

    cuentaMostrar = []

    for p in principalAccounts:
        for t in accountTransaccion:
            if p.id == t.account.id or p.id == t.account.parent.id or p.id == t.account.parent.parent.id:
                cuentaMostrar.append(p)
                break  # Rompe el bucle interno una vez que se encuentra una coincidencia

    return cuentaMostrar


def general_ledger_report(request):

    #Manda exclusivamente las cuentas que tengan ocurrencia en las partidas
    principalAccounts = cuentaToMayorizar()

    mayor = calculoMayor(principalAccounts)
    
    context = {
        'pricipalesCuentas' : principalAccounts,
        'detalleMayor' : mayor
    }
    
    return render(request, 'reports/ledger.html', context)



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

def mayorCuenta(principalAccounts):
    """
        Retorna las cuentas mayorizadas, no se toma en cuenta las partidas de cierre
    """
    journal = Transaction.objects.all()
    cuentasMayorizadas = []
    for a in principalAccounts:
        contador = 0.0 
        tipo  = Balance_type.objects.get(main_account=a.parent.parent) #Obetenemos el tipo que es True: Acreedor False: Deudor
        if not tipo.nature_of_balance:
            print(a.name,"Es deudor porque ",a.parent.parent.name,"lo es")
            for j in journal:
                if j.Item.isItemEnd is False:
                    if j.account.name == a.name or j.account.parent.name == a.name or j.account.parent.parent.name == a.name:
                        contador += getSaldo(j,True)
                        print("--------------",contador,"--------------",contador,"--------------",j.Item.value)
                        
        else:
            print(a.name,"Es acreedor porque ",a.parent.parent.name,"lo es")
            for j in journal:
                if j.Item.isItemEnd is False:
                    if j.account.name == a.name or j.account.parent.name == a.name or j.account.parent.parent.name == a.name:
                        contador += getSaldo(j,False)
                        print("--------------",contador,"--------------",contador,"--------------",j.Item.value)
        print("name: ",a.name," saldo: ",contador)
        cuentasMayorizadas.append({'main': a.name, 'saldo':contador})              
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
                        cuentasMayorizadas.append({'main': a.name, 'transaccion':j, 'saldo':contador, 'numero':num})              
    return cuentasMayorizadas


