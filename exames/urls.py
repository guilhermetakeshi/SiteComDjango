from django.urls import path
from . import views
# o ponto significa que eu quero importar as coisas daonde eu to, ou seja a pasta usuarios

urlpatterns = [
    path('solicitar_exames/', views.solicitar_exames, name="solicitar_exames"),
    # o primeiro parametro é o nome q vai ficar na url, 
    # o segundo é a função python que isso vai chamar,
    # o terceiro é a identificação
    path('fechar_pedido/', views.fechar_pedido, name="fechar_pedido"),
    path('gerenciar_pedidos/', views.gerenciar_pedidos, name="gerenciar_pedidos"),
    #url dinamica = 
    path('cancelar_pedido/<int:pedido_id>', views.cancelar_pedido, name = 'cancelar_pedido'),
    path('gerenciar_exames/', views.gerenciar_exames, name="gerenciar_exames"),
    path('permitir_abrir_exame/<int:exame_id>', views.permitir_abrir_exame, name="permitir_abrir_exame"),
    path('solicitar_senha_exame/<int:exame_id>', views.solicitar_senha_exame, name="solicitar_senha_exame"),
    path('gerar_acesso_medico/', views.gerar_acesso_medico, name="gerar_acesso_medico"),
    path('acesso_medico/<str:token>', views.acesso_medico, name="acesso_medico"),
]