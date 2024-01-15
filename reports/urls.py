from django.urls import path
from .views import majorJournal,chekingBalance
from stateOfResult.views import general_stateOfResult_report

urlpatterns = [
    path('libro_mayor/', majorJournal, name='major_journal'),
    path('balanza_comprobación/', chekingBalance, name='checkin_balance'),
    path('estado_de_resultado/', general_stateOfResult_report, name='general_stateOfResult_report'),
]