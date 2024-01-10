from django.urls import path
from . import views

urlpatterns = [
    path('',views.signIn),
    path('dashboard',views.dashBoard, name='dashboard')
]
