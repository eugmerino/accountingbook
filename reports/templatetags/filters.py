from django import template

from journal.models import Transaction
from catalogue.models import Account,Balance_type

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
