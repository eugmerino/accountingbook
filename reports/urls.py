from django.urls import path
from .views import chekingBalance,balanceGenereal,catalogo,libroDiario, ledgerView
from stateOfResult.views import stateOfResultView


urlpatterns = [
    path('libro_mayor/', ledgerView, name='ledgerView'),
    path('balanza_comprobación/', chekingBalance, name='checkin_balance'),
    path('balance_general/', balanceGenereal, name='general_balance'),
    path('estado_de_resultado/', stateOfResultView, name='state_of_result'),
    path('catalogo/', catalogo, name='catalogue'),
    path('libro_diario/', libroDiario, name='journal'),
]