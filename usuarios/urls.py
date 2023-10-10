from django.urls import path
from . import views
# o ponto significa que eu quero importar as coisas daonde eu to, ou seja a pasta usuarios

urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"),
    # o primeiro parametro é o nome q vai ficar na url, 
    # o segundo é a função python que isso vai chamar,
    # o terceiro é a identificação
    path('login/', views.logar, name="login"),
]