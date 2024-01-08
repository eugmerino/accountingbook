from django.urls import path
from . import views

urlpatterns = [
    path('',views.start),
    path('login/',views.signIn, name="login"),
    path('logout/',views.singOut, name="logout"),
    path('dashboard/',views.dashBoard, name='dashboard')
]
