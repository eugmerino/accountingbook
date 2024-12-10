from django.urls import path, include
from . import views

urlpatterns = [
    path('cuentas',views.accountView, name="accounts"),
    path('crearcuentas',views.createAccntView, name="createaccnt"),
    path('naturaleza',views.natureView, name="natures"),
    path('crearnaturaleza',views.createNaturView, name="createnature"),
]
