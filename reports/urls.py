from django.urls import path
from .views import general_ledger_report

urlpatterns = [
    path('libro_mayor/', general_ledger_report, name='general_ledger_report'),
]