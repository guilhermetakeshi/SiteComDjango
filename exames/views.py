from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from . models import TiposExames, PedidosExames, SolicitacaoExame, AcessoMedico
from datetime import datetime

# la nos users do django, tem uma verificação se o usuario é autenticado (logado) ou é anonimo, e precisamos disso
# pois os exames só podem ser acessados por alguem logado no sistema

# para ficar melhor, usaremos o decorador do python.django com o login_required


@login_required # isso verifica se o cara ta logado ou não
def solicitar_exames(request):
    #if request.user.is_authenticated:
    tipos_exames = TiposExames.objects.all()
    
    if request.method == 'GET':
        context = {'tipos_exames': tipos_exames}
        return render(request, 'solicitar_exames.html', context)
    
    elif request.method == 'POST':
        exames_id = request.POST.getlist('exames')
        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
        # o id__in busca todos os ID que estiver na lista de id dos exames, que foi pego do solicitar_exames.html
        # que o cliente clicou.s
        
        # preco_total = solicitacao_exames.aggregate(total=Sum('preco'))['total']
        preco_total = 0.00
        for i in solicitacao_exames:
            if i.disponivel == True:  # Verifica se o exame está disponível
                preco_total += i.preco

        return render(request, 'solicitar_exames.html', {'solicitacao_exames': solicitacao_exames, 
            'preco_total': preco_total, 'tipos_exames': tipos_exames})

@login_required
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
    
    pedido_exame = PedidosExames(
        usuario = request.user,
        data = datetime.now(),
    )
    pedido_exame.save()
    
    for exame in solicitacao_exames:
        solicitacao_exame_temp = SolicitacaoExame(
            usuario = request.user,
            exame = exame,
            status = "E"
        )
        solicitacao_exame_temp.save()
        pedido_exame.exames.add(solicitacao_exame_temp)
    
    pedido_exame.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido de Exame realizado com SUCESSO')
    return redirect('/exames/gerenciar_pedidos/')

@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})

@login_required
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id=pedido_id)

    if not pedido.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esse pedido não é seu')
        return redirect('/exames/gerenciar_pedidos/')

    pedido.agendado = False
    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido cancelado com sucesso')
    return redirect('/exames/gerenciar_pedidos/')

@login_required
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)

    return render(request, 'gerenciar_exames.html', {'exames': exames})

import os

@login_required
def permitir_abrir_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    if not exame.requer_senha:
        if os.path.exists(exame.resultado.path):
            return redirect(exame.resultado.url)
        else:
            messages.add_message(request, constants.ERROR, 'O resultado do exame não está disponível')
            return redirect('/exames/gerenciar_exames/')
    return redirect(f'exames/solicitar_senha_exame/{exame.id}')
        
@login_required
def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    if request.method == "GET":
        return render(request, 'solicitar_senha_exame.html', {'exame': exame})
    elif request.method == "POST":
        senha = request.POST.get("senha")
        # Verificar se o exame pertence ao usuário autenticado
        if exame.usuario == request.user:
            if senha == exame.senha:
                return redirect(exame.resultado.url)
            else:
                messages.add_message(request, constants.ERROR, 'Senha Inválida')
                return redirect(f'/exames/solicitar_senha_exame/{exame.id}')
        else:
            messages.add_message(request, constants.ERROR, 'Você não tem permissão para acessar este exame')
            return redirect('/exames/gerenciar_exames/')

@login_required
def gerar_acesso_medico(request):
    if request.method == "GET":
        acessos_medicos = AcessoMedico.objects.filter(usuario = request.user)
        return render(request, 'gerar_acesso_medico.html', {'acessos_medicos': acessos_medicos})
    elif request.method == "POST":
        identificacao = request.POST.get('identificacao')
        tempo_de_acesso = request.POST.get('tempo_de_acesso')
        data_exame_inicial = request.POST.get("data_exame_inicial")
        data_exame_final = request.POST.get("data_exame_final")

        acesso_medico = AcessoMedico(
            usuario = request.user,
            identificacao = identificacao,
            tempo_de_acesso = tempo_de_acesso,
            data_exames_iniciais = data_exame_inicial,
            data_exames_finais = data_exame_final,
            criado_em = datetime.now()
        )

        acesso_medico.save()

        messages.add_message(request, constants.SUCCESS, 'Acesso gerado com sucesso')
        return redirect('/exames/gerar_acesso_medico')


def acesso_medico(request, token):
    acesso_medico = AcessoMedico.objects.get(token=token)
    
    if acesso_medico.status == "Expirado":
        messages.add_message(request, constants.ERROR, 'Esse token já expirou, solicite outro')
        return redirect('/usuarios/login')
    
    pedidos = PedidosExames.objects.filter(usuario = acesso_medico.usuario).filter(
        data__gte = acesso_medico.data_exames_iniciais).filter(data__lt = acesso_medico.data_exames_finais)
    
    return render(request, 'acesso_medico.html', {'pedidos': pedidos})