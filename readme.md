    Readme - Configurações Iniciais
Este é um guia passo a passo para as configurações iniciais de um projeto Django chamado VitaLab. As configurações iniciais incluem a criação de um ambiente virtual, instalação do Django, criação de um aplicativo de usuário, configuração de estilos CSS, criação de modelos para exames e migrações.

    Criando o Ambiente Virtual
Primeiro, você precisa criar um ambiente virtual para isolar as dependências do seu projeto. Siga os comandos abaixo, dependendo do seu sistema operacional:

Linux:
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\Activate

Se você receber um erro de permissão ao executar os comandos acima, execute o seguinte comando no Windows antes de tentar novamente:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

Instalando o Django e Bibliotecas
Agora, instale o Django e as bibliotecas necessárias com os seguintes comandos:

pip install django
pip install pillow

Criando o Projeto Django
Vamos criar o projeto Django chamado "vitalab" com o seguinte comando:

django-admin startproject vitalab .

A seguir, execute o servidor de desenvolvimento para testar seu projeto:

python manage.py runserver

Criando o Aplicativo de Usuário
Vamos criar um aplicativo chamado "usuarios" para gerenciar o cadastro de usuários.

Primeiro, crie a URL para o aplicativo em seu arquivo de URL principal (geralmente chamado de "urls.py"):

# vitalab/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ... outras URLs ...
    path('usuarios/', include('usuarios.urls')),
]

Em seguida, crie o arquivo "urls.py" dentro do diretório "usuarios":

# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"),
]

Crie a função "cadastro" em "views.py" do aplicativo "usuarios":

# usuarios/views.py
from django.shortcuts import render

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')

Configure onde o Django irá procurar por arquivos .html:
os.path.join(BASE_DIR, 'templates')


Configurando Templates e Estilos
Crie um arquivo "base.html" em um diretório chamado "templates/bases" com o seguinte conteúdo:

{% load static %}
<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>VitaLab</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet">
    {% block 'head' %}{% endblock %}
</head>
<body>
    {% block 'conteudo' %}{% endblock %}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

Página de Cadastro (cadastro.html)
Agora, crie um arquivo "cadastro.html" em um diretório chamado "templates/usuarios" com o seguinte conteúdo:

{% extends "bases/base.html" %}
{% load static %}
{% block 'head' %}
{% endblock 'head' %}
{% block 'conteudo' %}
<br>
<br>
<div class="container">
    <h3 class="font-destaque">Cadastre-se</h3>
    <div class="row">
        <div class="col-md-3" style="text-align: center">
            <img src="" alt="">
            <h3>VitaLab</h3>
        </div>
        <div class="col-md-9">
            <form action="" method="POST">
                <label>Primeiro nome</label>
                <br>
                <input type="text" class="input-default" name="primeiro_nome">
                <br>
                <br>
                <label>Último nome</label>
                <br>
                <input type="text" class="input-default" name="ultimo_nome">
                <!-- ... outros campos de formulário ... -->
            </form>
        </div>
    </div>
    <!-- ... outros elementos HTML ... -->
</div>
{% endblock %}

Configurando CSS
Crie um arquivo chamado "base.css" em "templates/static/geral/css" com o seguinte conteúdo:

:root {
    --main-color: #151C34;
    --dark-color: #0C121C;
    --light-color: #6DE6EE;
    --contrast-color: #f4c96b;
    --differential-color: #066668;
}

body {
    color: white;
}

.font-destaque {
    color: var(--light-color);
    font-size: 40px;
}

.input-default {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--differential-color);
    padding: 7px;
    width: 50%;
}

.w100 {
    width: 100%;
}

.btn-default {
    background-color: var(--light-color);
    color: black;
    width: 15%;
    padding: 10px;
    border: none;
    border-radius: 10px;
}

.font-destaque-secundaria {
    color: var(--light-color);
    font-size: 35px;
}

Em "templates/static/usuarios/css", crie um arquivo chamado "css.css" com o seguinte conteúdo:

body {
    background-image: url('/static/geral/img/bg1.png');
    background-size: cover;
}

p {
    color: var(--light-color);
}

Imagens
Coloque a imagem "bg1.png" dentro de "templates/static/geral/img".

Importando CSS e Imagens
No arquivo "base.html", importe o arquivo CSS principal "base.css" adicionando a seguinte linha no cabeçalho:

<link href="{% static 'geral/css/base.css' %}" rel="stylesheet">

No arquivo "cadastro.html", importe o arquivo CSS específico para a página de cadastro:

<link href="{% static 'usuarios/css/css.css' %}" rel="stylesheet">

Além disso, adicione a logo da empresa ao HTML onde desejar:

<img src="{% static 'geral/img/logo.png' %}" alt="">

Executando Migrações
Após criar as models, execute as migrações para criar as tabelas do banco de dados:

python manage.py makemigrations
python manage.py migrate

Criando um Super Usuário
Crie um super usuário para acessar a área administrativa:

python manage.py createsuperuser

Configurando a Área Administrativa
Registre as models criadas na área administrativa editando o arquivo "admin.py" do aplicativo "exames":

# exames/admin.py
from django.contrib import admin
from .models import TiposExames, PedidosExames, SolicitacaoExame

admin.site.register(TiposExames)
admin.site.register(PedidosExames)
admin.site.register(SolicitacaoExame)

Agora você deve estar pronto para continuar o desenvolvimento do seu projeto Django VitaLab com funcionalidades de cadastro de usuários e gerenciamento de exames. Certifique-se de ajustar o código e os templates de acordo com suas necessidades específicas.