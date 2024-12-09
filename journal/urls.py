from django.urls import path
from . import views

urlpatterns = [
    path('partidas', views.journalMain, name='journalMain'),
    path('partida', views.formItem, name='formItem'),
    path('partida/editar/<int:pk>/', views.editItem, name='editItem'),
    path('partida/eliminar/<int:pk>/', views.deleteItem, name='deleteItem'),
]
