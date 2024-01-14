from django.urls import path
from .views import general_ledger_report
from stateOfResult.views import general_stateOfResult_report

urlpatterns = [
    path('libro_mayor/', general_ledger_report, name='general_ledger_report'),
    path('estado_de_resultado/', general_stateOfResult_report, name='general_stateOfResult_report'),
]