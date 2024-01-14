from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.start),
    path('login/',views.signIn, name="login"),
    path('logout/',views.singOut, name="logout"),
    path('home/',views.dashBoard, name='home'),
    path('home/',include('catalogue.urls'))
]
