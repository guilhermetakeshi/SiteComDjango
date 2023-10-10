# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
# isso faz a busca no django de uma model de autentificação de Users
# pois as vies se comunicam com as models e se n tivesse isso automatico, iriamos terq criar do 0

from django.contrib.messages import constants # aqui é importado os alertas de menssagem do django
from django.contrib import messages # aqui importa as msg que a gente alterou pelas settings.py  

from django.contrib.auth import authenticate, login # faz a importação de um authenticador automatico do django


# aqui cria as funções python que iremos utilizar, mencionadas no usuarios/urls.py
'''
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
        # o render, faz a função de rendenizar os templates que passamos no arquivo html
    elif request.method == "POST":
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        # TODO: validar se o username do usuario já existe
        try:
            user = User.objects.create_user(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                username = username,
                email = email,
                password = senha
                # o django faz automaticamente a HASH da senha com algoritimos
            )
        except:
            # aqui é a msg de erro, e pra isso, podemos usar o sistema de menssagens do django
            messages.add_message(request, constants.ERROR, 'Erro desconhecido, contate um administrador') 
            return redirect('/usuarios/cadastro') 
            
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos 6 caracteres') 
            return render(request, 'cadastro.html')
        
        if primeiro_nome and email and senha and confirmar_senha:
            if senha == confirmar_senha:
                messages.add_message(request, constants.SUCCESS, 'Usuário alvo com SUCESSO') 
                return render(request, 'login.html')
            else:
                #return render(request, 'cadastro_erro.html')
                messages.add_message(request, constants.ERROR, 'As senhas não coincidem')  
                return redirect('/usuarios/cadastro')
        else:
            return render(request, 'cadastro.html')
'''
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:    
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            return redirect('/usuarios/cadastro')
        
        try:
            # Username deve ser único!
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
        except:
            return redirect('/usuarios/cadastro')


        return redirect('/usuarios/cadastro')

def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('/usuarios/login')