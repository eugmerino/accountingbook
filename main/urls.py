from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.start,name='start'),
    path('login/',views.signIn, name="login"),
    path('logout/',views.singOut, name="logout"),
    path('home/',views.dashBoard, name='home'),
    path('catalogo/',include('catalogue.urls')),
    path('libro_diario/',include('journal.urls'))
]
