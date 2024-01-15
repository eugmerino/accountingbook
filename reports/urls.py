from django.urls import path
from .views import majorJournal,chekingBalance

urlpatterns = [
    path('libro_mayor/', majorJournal, name='major_journal'),
    path('balanza_comprobación/', chekingBalance, name='checkin_balance'),
]