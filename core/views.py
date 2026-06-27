import json
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import RegistroJogada, BancoQuestao

# --- SISTEMA DE ACESSO ---
def login_view(request):
    erro = None
    if request.method == 'POST':
        usuario_digitado = request.POST.get('usuario')
        senha_digitada = request.POST.get('senha')
        user = authenticate(request, username=usuario_digitado, password=senha_digitada)
        if user is not None:
            login(request, user)
            # Se já tem ano na sessão, vai direto para home
            if request.session.get('ano_selecionado'):
                return redirect('home')
            return redirect('selecionar_ano')
        else:
            erro = "E-mail ou senha incorretos. Tente novamente!"
    return render(request, 'login.html', {'erro': erro})

def logout_view(request):
    logout(request)
    return redirect('login')

def registro_view(request):
    erro = None
    sucesso = None
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if not email.endswith('@csanl.com.br'):
            erro = "Acesso negado: Utilize o e-mail oficial do colégio (@csanl.com.br)."
        elif User.objects.filter(username=email).exists():
            erro = "Este e-mail já está cadastrado!"
        else:
            user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
            user.save()
            sucesso = "Aluno cadastrado com sucesso! Faça o login."
    return render(request, 'registro.html', {'erro': erro, 'sucesso': sucesso})

# --- TELAS DE NAVEGAÇÃO DO PORTAL ---
@login_required(login_url='/')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/')
def menu_portugues(request):
    return render(request, 'menu_portugues.html')

@login_required(login_url='/')
def menu_ingles(request):
    return render(request, 'menu_ingles.html')

@login_required(login_url='/')
def matematica(request):
    return render(request, 'matematica.html')

@login_required(login_url='/')
def niveis_adicao(request):
    return render(request, 'niveis_adicao.html')

@login_required(login_url='/')
def niveis_subtracao(request):
    return render(request, 'niveis_subtracao.html')

@login_required(login_url='/')
def niveis_multiplicacao(request):
    return render(request, 'niveis_multiplicacao.html')

@login_required(login_url='/')
def niveis_divisao(request):
    return render(request, 'niveis_divisao.html')

@login_required(login_url='/')
def niveis_potenciacao(request):
    return render(request, 'niveis_potenciacao.html')

# --- O PAINEL DE RELATÓRIO RECONSTRUÍDO ---
@login_required(login_url='/')
def relatorio_desempenho(request):
    jogadas = RegistroJogada.objects.filter(jogador=request.user)
    total_geral = jogadas.count()
    
    estatisticas_matematica = []
    estatisticas_ingles = []
    estatisticas_portugues = []
    
    if total_geral > 0:
        operacoes_math = ['adicao', 'subtracao', 'multiplicacao', 'divisao']
        icones_math = {'adicao': '➕', 'subtracao': '➖', 'multiplicacao': '✖️', 'divisao': '➗'}
        for op in operacoes_math:
            jogadas_op = jogadas.filter(operacao=op)
            if jogadas_op.count() > 0:
                acertos = jogadas_op.filter(acertou=True).count()
                taxa = (acertos / jogadas_op.count()) * 100
                tempo_medio = jogadas_op.aggregate(Avg('tempo_segundos'))['tempo_segundos__avg']
                estatisticas_matematica.append({
                    'operacao': op.capitalize(), 'icone': icones_math[op], 'total': jogadas_op.count(),
                    'acertos': acertos, 'erros': jogadas_op.count() - acertos,
                    'taxa_acerto': round(taxa, 1), 'tempo_medio': round(tempo_medio, 1) if tempo_medio else 0
                })
        
        jogos_ingles = [('ingles', 'Vocabulário (Palavras)'), ('ingles_frases', 'Completar Frases')]
        for op_id, nome_op in jogos_ingles:
            jogadas_op = jogadas.filter(operacao=op_id)
            if jogadas_op.count() > 0:
                rodadas_perfeitas = jogadas_op.filter(acertou=True).count()
                taxa_op = (rodadas_perfeitas / jogadas_op.count()) * 100
                tempo_medio = jogadas_op.aggregate(Avg('tempo_segundos'))['tempo_segundos__avg']
                estatisticas_ingles.append({
                    'nome': nome_op, 'total_rodadas': jogadas_op.count(), 'rodadas_perfeitas': rodadas_perfeitas,
                    'taxa_perfeicao': round(taxa_op, 1), 'tempo_medio': round(tempo_medio, 1) if tempo_medio else 0
                })

        jogos_portugues = [
            ('portugues_ortografia', 'ortografia_questao', 'Ortografia', '✏️'),
            ('portugues_silaba', 'silaba_tonica_questao', 'Sílaba Tônica', '🗣️'),
            ('portugues_sinonimos', 'antonimos_questao', 'Sinônimos/Antônimos', '🔄'),
            ('portugues_silabas', 'contagem_questao', 'Caçador de Sílabas', '✂️'),
            ('portugues_gramatica', 'nivel2_questao', 'Detetive de Palavras', '🔎'),
            ('portugues_encontros_vocalicos', 'encontros_vocalicos_questao', 'Encontros Vocálicos', '🔤'),
            ('portugues_digrafo', 'digrafos_questao', 'Dígrafos', '🔡')
        ]
        for op_id, nivel_id, nome_op, icone_op in jogos_portugues:
            jogadas_op = jogadas.filter(operacao=op_id, nivel=nivel_id)
            if jogadas_op.count() > 0:
                acertos_op = jogadas_op.filter(acertou=True).count()
                taxa_op = (acertos_op / jogadas_op.count()) * 100
                tempo_medio = jogadas_op.aggregate(Avg('tempo_segundos'))['tempo_segundos__avg']
                estatisticas_portugues.append({
                    'nome': nome_op, 'icone': icone_op,
                    'total': jogadas_op.count(), 'acertos': acertos_op,
                    'erros': jogadas_op.count() - acertos_op,
                    'taxa_acerto': round(taxa_op, 1), 'tempo_medio': round(tempo_medio, 1) if tempo_medio else 0
                })

    contexto = {
        'total_geral': total_geral,
        'estatisticas': estatisticas_matematica,
        'estatisticas_ingles': estatisticas_ingles,
        'estatisticas_portugues': estatisticas_portugues
    }
    return render(request, 'relatorio.html', contexto)

# --- O JOGO INTELIGENTE ---
@login_required(login_url='/')
def jogo_tabuada(request, operacao, nivel):
    contexto = {'operacao': operacao, 'nivel': nivel}
    return render(request, 'jogo.html', contexto)

@csrf_exempt
def salvar_jogada(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            usuario_logado = request.user if request.user.is_authenticated else None
            RegistroJogada.objects.create(
                jogador=usuario_logado, operacao=dados.get('operacao', 'multiplicacao'),
                nivel=dados.get('nivel', 'unidades'), numero_1=dados.get('numero_1', 0),
                numero_2=dados.get('numero_2', 0), resposta_aluno=dados.get('resposta_aluno', '0'),
                acertou=dados.get('acertou', True), tempo_segundos=dados.get('tempo_segundos', 0)
            )
            return JsonResponse({'status': 'sucesso'})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)})
    return JsonResponse({'status': 'metodo_invalido'})

# --- MÓDULO DE INGLÊS ---
@login_required(login_url='/')
def ingles_vocabulario(request):
    vocabulario = [
        {'palavra': 'Dog', 'emoji': '🐶'}, {'palavra': 'Cat', 'emoji': '🐱'}, 
        {'palavra': 'Spider', 'emoji': '🕷️'}, {'palavra': 'Mouse', 'emoji': '🐭'},
        {'palavra': 'Bird', 'emoji': '🐦'}, {'palavra': 'Lion', 'emoji': '🦁'},
        {'palavra': 'Fish', 'emoji': '🐟'}, {'palavra': 'Chicken', 'emoji': '🐔'},
        {'palavra': 'Elephant', 'emoji': '🐘'}, {'palavra': 'School', 'emoji': '🏫'}, 
        {'palavra': 'Book', 'emoji': '📖'}, {'palavra': 'Pencil', 'emoji': '✏️'}, 
        {'palavra': 'Computer', 'emoji': '💻'}, {'palavra': 'Chair', 'emoji': '🪑'}, 
        {'palavra': 'Classroom', 'emoji': '🧑‍🏫'}, {'palavra': 'Student', 'emoji': '🎒'},
        {'palavra': 'Earth', 'emoji': '🌍'}, {'palavra': 'Sun', 'emoji': '☀️'},
        {'palavra': 'Moon', 'emoji': '🌙'}, {'palavra': 'Rain', 'emoji': '🌧️'},
        {'palavra': 'Tree', 'emoji': '🌳'}, {'palavra': 'River', 'emoji': '🏞️'},
        {'palavra': 'Fire', 'emoji': '🔥'}, {'palavra': 'Snow', 'emoji': '❄️'},
        {'palavra': 'Wind', 'emoji': '🌬️'}, {'palavra': 'Beach', 'emoji': '🏖️'},
        {'palavra': 'Car', 'emoji': '🚗'}, {'palavra': 'Airplane', 'emoji': '✈️'},
        {'palavra': 'Bus', 'emoji': '🚌'}, {'palavra': 'Building', 'emoji': '🏢'},
        {'palavra': 'Church', 'emoji': '⛪'}, {'palavra': 'House', 'emoji': '🏠'}, 
        {'palavra': 'Door', 'emoji': '🚪'}, {'palavra': 'Kitchen', 'emoji': '🍽️'}, 
        {'palavra': 'Bedroom', 'emoji': '🛏️'}, {'palavra': 'Lamp', 'emoji': '💡'}, 
        {'palavra': 'Window', 'emoji': '🪟'}, {'palavra': 'Umbrella', 'emoji': '☔'}, 
        {'palavra': 'Table', 'emoji': '/static/img/table.png', 'is_image': True},
        {'palavra': 'Orange', 'emoji': '🍊'}, {'palavra': 'Apple', 'emoji': '🍎'},
        {'palavra': 'Potato', 'emoji': '🥔'}, {'palavra': 'Banana', 'emoji': '🍌'},
        {'palavra': 'Pineapple', 'emoji': '🍍'}, {'palavra': 'Onion', 'emoji': '🧅'},
        {'palavra': 'Tomato', 'emoji': '🍅'}, {'palavra': 'Mango', 'emoji': '🥭'},
        {'palavra': 'Hat', 'emoji': '🎩'}, {'palavra': 'Shorts', 'emoji': '🩳'},
        {'palavra': 'Shirt', 'emoji': '👕'}, {'palavra': 'Pants', 'emoji': '👖'},
        {'palavra': 'Jacket', 'emoji': '🧥'}, {'palavra': 'Shoes', 'emoji': '👞'},
        {'palavra': 'Foot', 'emoji': '🦶'}, {'palavra': 'Feet', 'emoji': '👣'},
        {'palavra': 'Hand', 'emoji': '🖐️'}, {'palavra': 'Eye', 'emoji': '👁️'},
        {'palavra': 'Head', 'emoji': '👤'}, {'palavra': 'Hair', 'emoji': '💇'},
        {'palavra': 'Leg', 'emoji': '🦵'}, {'palavra': 'Nose', 'emoji': '👃'},
        {'palavra': 'Mouth', 'emoji': '👄'}, {'palavra': 'Ear', 'emoji': '👂'},
        {'palavra': 'Red', 'emoji': '🔴'}, {'palavra': 'Blue', 'emoji': '🔵'},
        {'palavra': 'Happy', 'emoji': '😄'}, {'palavra': 'Sad', 'emoji': '😢'},
        {'palavra': 'Play soccer', 'emoji': '⚽'}, {'palavra': 'Ride a bike', 'emoji': '🚲'},
        {'palavra': 'Basketball', 'emoji': '🏀'}, {'palavra': 'Chess game', 'emoji': '♟️'}
    ]
    itens_jogo = random.sample(vocabulario, 12)
    palavras = [item['palavra'] for item in itens_jogo]
    imagens = itens_jogo.copy()
    random.shuffle(palavras)
    random.shuffle(imagens)
    contexto = {'palavras': palavras, 'imagens': imagens}
    return render(request, 'ingles_drag_drop.html', contexto)

@login_required(login_url='/')
def ingles_frases(request):
    distratores = ['apple', 'book', 'car', 'blue', 'rain', 'house', 'spider', 'table', 'shoes', 'onion', 'happy', 'pencil', 'door', 'water', 'sun', 'moon', 'bird', 'lion', 'church', 'building', 'nose', 'ear', 'jacket', 'bus', 'red', 'tree', 'bike', 'sunny', 'cloudy', 'windy', 'hot', 'cold', 'rainy', 'warm']
    templates = [
        {'frase': 'Do you have a pet ______?', 'variacoes': [{'resposta': 'dog', 'emoji': '🐶'}, {'resposta': 'cat', 'emoji': '🐱'}, {'resposta': 'mouse', 'emoji': '🐭'}, {'resposta': 'fish', 'emoji': '🐟'}]},
        {'frase': 'My favorite fruit is ______.', 'variacoes': [{'resposta': 'apple', 'emoji': '🍎'}, {'resposta': 'banana', 'emoji': '🍌'}, {'resposta': 'pineapple', 'emoji': '🍍'}, {'resposta': 'mango', 'emoji': '🥭'}, {'resposta': 'orange', 'emoji': '🍊'}]},
        {'frase': 'The book is on the ______.', 'variacoes': [{'resposta': 'table', 'emoji': '/static/img/table.png', 'is_image': True}]},
        {'frase': 'He likes to play ______.', 'variacoes': [{'resposta': 'soccer', 'emoji': '⚽'}, {'resposta': 'basketball', 'emoji': '🏀'}, {'resposta': 'chess', 'emoji': '♟️'}]},
        {'frase': 'Are you going to the ______?', 'variacoes': [{'resposta': 'beach', 'emoji': '🏖️'}, {'resposta': 'church', 'emoji': '⛪'}, {'resposta': 'house', 'emoji': '🏠'}, {'resposta': 'school', 'emoji': '🏫'}]},
        {'frase': 'I like to ______ in the park.', 'variacoes': [{'resposta': 'ride a bike', 'emoji': '🚲'}, {'resposta': 'play soccer', 'emoji': '⚽'}, {'resposta': 'swim', 'emoji': '🏊'}, {'resposta': 'rollerblade', 'emoji': '🛼'}]},
        {'frase': 'The color of the sky is ______.', 'variacoes': [{'resposta': 'blue', 'emoji': '☁️'}]},
        {'frase': 'The ______ is yellow.', 'variacoes': [{'resposta': 'sun', 'emoji': '☀️'}, {'resposta': 'banana', 'emoji': '🍌'}]},
        {'frase': 'She is wearing a beautiful ______.', 'variacoes': [{'resposta': 'shirt', 'emoji': '👕'}, {'resposta': 'jacket', 'emoji': '🧥'}, {'resposta': 'hat', 'emoji': '🎩'}]},
        {'frase': 'The weather today is ______.', 'variacoes': [{'resposta': 'sunny', 'emoji': '☀️'}, {'resposta': 'cloudy', 'emoji': '☁️'}, {'resposta': 'windy', 'emoji': '🌬️'}, {'resposta': 'rainy', 'emoji': '🌧️'}]},
        {'frase': 'I need a jacket because it is very ______!', 'variacoes': [{'resposta': 'cold', 'emoji': '🥶'}, {'resposta': 'windy', 'emoji': '🌬️'}]},
        {'frase': 'Let\'s go to the beach! It is so ______ today.', 'variacoes': [{'resposta': 'hot', 'emoji': '🥵'}, {'resposta': 'warm', 'emoji': '😎'}, {'resposta': 'sunny', 'emoji': '☀️'}]}
    ]
    moldes_escolhidos = random.sample(templates, min(8, len(templates)))
    frases_geradas = []
    for molde in moldes_escolhidos:
        var_escolhida = random.choice(molde['variacoes'])
        resposta_certa = var_escolhida['resposta']
        opcoes_erradas = random.sample([d for d in distratores if d != resposta_certa], 3)
        opcoes_finais = opcoes_erradas + [resposta_certa]
        random.shuffle(opcoes_finais)
        frases_geradas.append({'frase': molde['frase'], 'resposta': resposta_certa, 'opcoes': opcoes_finais, 'emoji': var_escolhida['emoji']})
    contexto = {'frases_json': json.dumps(frases_geradas)}
    return render(request, 'ingles_frases.html', contexto)

# --- MÓDULO DE PORTUGUÊS ---
@login_required(login_url='/')
def portugues_ortografia(request):
    banco_palavras = [
        {'palavra': 'CA___ORRO', 'resposta': 'CH', 'opcoes': ['X', 'CH', 'SH']},
        {'palavra': 'PÁ___ARO', 'resposta': 'SS', 'opcoes': ['S', 'SS', 'Ç']},
        {'palavra': 'E___ELENTE', 'resposta': 'XC', 'opcoes': ['C', 'S', 'XC']},
        {'palavra': 'A___ÚCAR', 'resposta': 'Ç', 'opcoes': ['S', 'SS', 'Ç']},
        {'palavra': 'GIRA___OL', 'resposta': 'SS', 'opcoes': ['S', 'SS', 'Ç']},
        {'palavra': '___INÁSTICA', 'resposta': 'G', 'opcoes': ['G', 'J']},
        {'palavra': 'MA___ESTADE', 'resposta': 'J', 'opcoes': ['G', 'J']},
        {'palavra': 'FA___INA', 'resposta': 'X', 'opcoes': ['X', 'CH', 'S']},
        {'palavra': 'CENOU___A', 'resposta': 'R', 'opcoes': ['R', 'RR']},
        {'palavra': 'CA___O (automóvel)', 'resposta': 'RR', 'opcoes': ['R', 'RR']},
        {'palavra': '___ACARÉ', 'resposta': 'J', 'opcoes': ['G', 'J']},
        {'palavra': '___ÍCARA', 'resposta': 'X', 'opcoes': ['X', 'CH', 'SS']},
    ]
    itens_jogo = random.sample(banco_palavras, 10)
    for item in itens_jogo:
        random.shuffle(item['opcoes'])
    contexto = {'palavras_json': json.dumps(itens_jogo)}
    return render(request, 'portugues_ortografia.html', contexto)

@login_required(login_url='/')
def portugues_silaba(request):
    banco_palavras = [
        # Oxítonas
        {'palavra': 'CAFÉ', 'resposta': 'Oxítona'},
        {'palavra': 'AMOR', 'resposta': 'Oxítona'},
        {'palavra': 'PORTUGUÊS', 'resposta': 'Oxítona'},
        {'palavra': 'COMPUTADOR', 'resposta': 'Oxítona'},
        {'palavra': 'FELIZ', 'resposta': 'Oxítona'},
        {'palavra': 'FUTEBOL', 'resposta': 'Oxítona'},
        {'palavra': 'JACARÉ', 'resposta': 'Oxítona'},
        {'palavra': 'ANIMAL', 'resposta': 'Oxítona'},
        {'palavra': 'CORAÇÃO', 'resposta': 'Oxítona'},
        {'palavra': 'PAPEL', 'resposta': 'Oxítona'},
        {'palavra': 'INVESTIR', 'resposta': 'Oxítona'},
        {'palavra': 'JOGAR', 'resposta': 'Oxítona'},
        {'palavra': 'ABACAXI', 'resposta': 'Oxítona'},
        {'palavra': 'GIBI', 'resposta': 'Oxítona'},
        {'palavra': 'CHAPÉU', 'resposta': 'Oxítona'},
        
        # Paroxítonas
        {'palavra': 'MENINO', 'resposta': 'Paroxítona'},
        {'palavra': 'MESA', 'resposta': 'Paroxítona'},
        {'palavra': 'LÁPIS', 'resposta': 'Paroxítona'},
        {'palavra': 'FÁCIL', 'resposta': 'Paroxítona'},
        {'palavra': 'JANELA', 'resposta': 'Paroxítona'},
        {'palavra': 'LEGO', 'resposta': 'Paroxítona'},
        {'palavra': 'FERRARI', 'resposta': 'Paroxítona'},
        {'palavra': 'MERCEDES', 'resposta': 'Paroxítona'},
        {'palavra': 'CRAQUE', 'resposta': 'Paroxítona'},
        {'palavra': 'PRAIA', 'resposta': 'Paroxítona'},
        {'palavra': 'PRANCHA', 'resposta': 'Paroxítona'},
        {'palavra': 'PLANILHA', 'resposta': 'Paroxítona'},
        {'palavra': 'ESCOLINHA', 'resposta': 'Paroxítona'},
        {'palavra': 'TECLADO', 'resposta': 'Paroxítona'},
        {'palavra': 'CAVALEIRO', 'resposta': 'Paroxítona'},
        
        # Proparoxítonas
        {'palavra': 'MÁGICO', 'resposta': 'Proparoxítona'},
        {'palavra': 'ÁRVORE', 'resposta': 'Proparoxítona'},
        {'palavra': 'LÂMPADA', 'resposta': 'Proparoxítona'},
        {'palavra': 'PÁSSARO', 'resposta': 'Proparoxítona'},
        {'palavra': 'MÉDICO', 'resposta': 'Proparoxítona'},
        {'palavra': 'ESTATÍSTICA', 'resposta': 'Proparoxítona'},
        {'palavra': 'MÉXICO', 'resposta': 'Proparoxítona'},
        {'palavra': 'GRÁFICO', 'resposta': 'Proparoxítona'},
        {'palavra': 'MAURÍCIO', 'resposta': 'Proparoxítona'},
        {'palavra': 'MATEMÁTICA', 'resposta': 'Proparoxítona'},
        {'palavra': 'DÚVIDA', 'resposta': 'Proparoxítona'},
        {'palavra': 'ÍNDICE', 'resposta': 'Proparoxítona'},
        {'palavra': 'GINÁSTICA', 'resposta': 'Proparoxítona'},
        {'palavra': 'RÁPIDO', 'resposta': 'Proparoxítona'},
        {'palavra': 'RELÂMPAGO', 'resposta': 'Proparoxítona'},
        {'palavra': 'CÍRCULO', 'resposta': 'Proparoxítona'},
        {'palavra': 'BÚSSOLA', 'resposta': 'Proparoxítona'},
    ]
    itens_jogo = random.sample(banco_palavras, 10)
    contexto = {'palavras_json': json.dumps(itens_jogo)}
    return render(request, 'portugues_silaba.html', contexto)

@login_required(login_url='/')
def portugues_sinonimos(request):
    banco_pares = [
        {'palavra': 'RÁPIDO', 'oposto': 'LENTO'}, {'palavra': 'QUENTE', 'oposto': 'FRIO'},
        {'palavra': 'LONGE', 'oposto': 'PERTO'}, {'palavra': 'GRANDE', 'oposto': 'PEQUENO'},
        {'palavra': 'DIA', 'oposto': 'NOITE'}, {'palavra': 'BOM', 'oposto': 'MAU'},
        {'palavra': 'CLARO', 'oposto': 'ESCURO'}, {'palavra': 'CHEIO', 'oposto': 'VAZIO'},
        {'palavra': 'ALTO', 'oposto': 'BAIXO'}, {'palavra': 'FORTE', 'oposto': 'FRACO'},
        {'palavra': 'FELIZ', 'oposto': 'TRISTE'}, {'palavra': 'FÁCIL', 'oposto': 'DIFÍCIL'},
        {'palavra': 'GIGANTE', 'oposto': 'MINÚSCULO'}, {'palavra': 'BARULHO', 'oposto': 'SILÊNCIO'},
        {'palavra': 'GORDO', 'oposto': 'MAGRO'}, {'palavra': 'GROSSO', 'oposto': 'FINO'},
        {'palavra': 'BONITO', 'oposto': 'FEIO'}, {'palavra': 'LIMPO', 'oposto': 'SUJO'},
    ]
    itens_jogo = random.sample(banco_pares, 10)
    palavras_arrastar = itens_jogo.copy()
    palavras_alvo = itens_jogo.copy()
    random.shuffle(palavras_arrastar)
    random.shuffle(palavras_alvo)
    contexto = {'palavras_arrastar': palavras_arrastar, 'palavras_alvo': palavras_alvo}
    return render(request, 'portugues_sinonimos.html', contexto)

@login_required(login_url='/')
def portugues_silabas(request):
    banco_palavras = [
        # 1 Sílaba
        {'palavra': 'SOL', 'separacao': 'SOL', 'resposta': 1},
        {'palavra': 'MAR', 'separacao': 'MAR', 'resposta': 1},
        {'palavra': 'GOL', 'separacao': 'GOL', 'resposta': 1},
        {'palavra': 'PAI', 'separacao': 'PAI', 'resposta': 1},
        
        # 2 Sílabas
        {'palavra': 'LEGO', 'separacao': 'LE-GO', 'resposta': 2},
        {'palavra': 'CRAQUE', 'separacao': 'CRA-QUE', 'resposta': 2},
        {'palavra': 'PRAIA', 'separacao': 'PRAI-A', 'resposta': 2},
        {'palavra': 'CARRO', 'separacao': 'CAR-RO', 'resposta': 2},
        {'palavra': 'BOLA', 'separacao': 'BO-LA', 'resposta': 2},
        {'palavra': 'LIVRO', 'separacao': 'LI-VRO', 'resposta': 2},
        
        # 3 Sílabas
        {'palavra': 'FERRARI', 'separacao': 'FER-RA-RI', 'resposta': 3},
        {'palavra': 'MERCEDES', 'separacao': 'MER-CE-DES', 'resposta': 3},
        {'palavra': 'FUTEBOL', 'separacao': 'FU-TE-BOL', 'resposta': 3},
        {'palavra': 'ESTAÇÃO', 'separacao': 'ES-TA-ÇÃO', 'resposta': 3},
        {'palavra': 'MÉXICO', 'separacao': 'MÉ-XI-CO', 'resposta': 3},
        {'palavra': 'PLANILHA', 'separacao': 'PLA-NI-LHA', 'resposta': 3},
        {'palavra': 'MOCHILA', 'separacao': 'MO-CHI-LA', 'resposta': 3},
        {'palavra': 'CELULAR', 'separacao': 'CE-LU-LAR', 'resposta': 3},
        
        # 4 Sílabas
        {'palavra': 'ESCOLINHA', 'separacao': 'ES-CO-LI-NHA', 'resposta': 4},
        {'palavra': 'FILIPINAS', 'separacao': 'FI-LI-PI-NAS', 'resposta': 4},
        {'palavra': 'AVENTURA', 'separacao': 'A-VEN-TU-RA', 'resposta': 4},
        {'palavra': 'BRINCADEIRA', 'separacao': 'BRIN-CA-DEI-RA', 'resposta': 4},
        {'palavra': 'COMPUTADOR', 'separacao': 'COM-PU-TA-DOR', 'resposta': 4},
        
        # 5 Sílabas ou mais
        {'palavra': 'ESTATÍSTICA', 'separacao': 'ES-TA-TÍS-TI-CA', 'resposta': 5},
        {'palavra': 'INVESTIMENTO', 'separacao': 'IN-VES-TI-MEN-TO', 'resposta': 5},
        {'palavra': 'MATEMÁTICA', 'separacao': 'MA-TE-MÁ-TI-CA', 'resposta': 5}
    ]
    itens_jogo = random.sample(banco_palavras, 10)
    contexto = {'palavras_json': json.dumps(itens_jogo)}
    return render(request, 'portugues_silabas.html', contexto)

@login_required(login_url='/')
def portugues_gramatica(request):
    banco_questoes = [
        {
            'pergunta': 'Na frase: "O peixe azul enfeita o aquário redondo.", quais palavras são os ADJETIVOS?',
            'resposta': 'azul e redondo',
            'opcoes': ['peixe e aquário', 'azul e redondo', 'enfeita e redondo', 'O e azul']
        },
        {
            'pergunta': 'Na frase: "A geladeira branca estava cheia de comidas gostosas.", quais são os SUBSTANTIVOS COMUNS?',
            'resposta': 'geladeira e comidas',
            'opcoes': ['branca e gostosas', 'estava e cheia', 'geladeira e comidas', 'A e de']
        },
        {
            'pergunta': 'Na frase: "Os meninos Gabriel e Lucas cuidam dos seus velhos brinquedos.", quais são os SUBSTANTIVOS PRÓPRIOS?',
            'resposta': 'Gabriel e Lucas',
            'opcoes': ['meninos e brinquedos', 'velhos e cuidam', 'Gabriel e Lucas', 'Os e dos']
        },
        {
            'pergunta': 'Na frase: "A mamãe Joana viu os passarinhos tristes na gaiola fria.", quais são os ADJETIVOS?',
            'resposta': 'tristes e fria',
            'opcoes': ['mamãe e gaiola', 'Joana e passarinhos', 'tristes e fria', 'viu e na']
        },
        {
            'pergunta': 'Na frase: "Lucas montou um enorme carro da Ferrari.", quais são os SUBSTANTIVOS PRÓPRIOS?',
            'resposta': 'Lucas e Ferrari',
            'opcoes': ['carro e enorme', 'Lucas e Ferrari', 'montou e um', 'enorme e carro']
        },
        {
            'pergunta': 'Na frase: "As belas praias do México têm águas cristalinas.", quais palavras são os ADJETIVOS?',
            'resposta': 'belas e cristalinas',
            'opcoes': ['praias e águas', 'belas e cristalinas', 'México e águas', 'As e do']
        },
        {
            'pergunta': 'Na frase: "O menino corajoso pratica kitesurf no mar agitado.", quais são os SUBSTANTIVOS COMUNS?',
            'resposta': 'menino, kitesurf e mar',
            'opcoes': ['corajoso e agitado', 'O e no', 'menino, kitesurf e mar', 'pratica e corajoso']
        },
        {
            'pergunta': 'Na frase: "A Mercedes prateada venceu a corrida difícil.", quais palavras são os ADJETIVOS?',
            'resposta': 'prateada e difícil',
            'opcoes': ['Mercedes e corrida', 'venceu e a', 'prateada e difícil', 'prateada e corrida']
        },
        {
            'pergunta': 'Na frase: "A bola novinha rolou para o gol vazio.", quais são os SUBSTANTIVOS COMUNS?',
            'resposta': 'bola e gol',
            'opcoes': ['novinha e vazio', 'rolou e para', 'bola e gol', 'A e o']
        },
        {
            'pergunta': 'Na frase: "O talentoso jogador marcou na Escolinha do bairro.", quais são os ADJETIVOS?',
            'resposta': 'talentoso',
            'opcoes': ['jogador', 'Escolinha', 'bairro', 'talentoso']
        }
    ]
    itens_jogo = random.sample(banco_questoes, min(8, len(banco_questoes)))
    for item in itens_jogo:
        random.shuffle(item['opcoes'])
    contexto = {'questoes_json': json.dumps(itens_jogo)}
    return render(request, 'portugues_gramatica.html', contexto)


@login_required(login_url='/')
def portugues_encontros_vocalicos(request):
    return render(request, 'portugues_encontros_vocalicos.html')


@login_required(login_url='/')
def portugues_digrafo(request):
    return render(request, 'portugues_digrafo.html')

# --- MÓDULO DE GEOGRAFIA ---
@login_required(login_url='/')
def menu_geografia(request):
    return render(request, 'menu_geografia.html')

@login_required(login_url='/')
def geografia_mapa(request):
    return render(request, 'geografia_mapa.html')

@login_required(login_url='/')
def geografia_quiz(request):
    banco_questoes = [
        {
            'pergunta': 'O que é Agricultura Familiar (ou de Subsistência)?',
            'resposta': 'Produção em pequenas propriedades feita por famílias.',
            'opcoes': ['Produção apenas para exportar para outros países.', 'Produção em pequenas propriedades feita por famílias.', 'Plantação de apenas um tipo de alimento.', 'Criação de gado em fazendas gigantes.']
        },
        {
            'pergunta': 'Qual é a principal característica da Grande Agricultura Comercial?',
            'resposta': 'Alta produção voltada para exportação.',
            'opcoes': ['Produção feita sem o uso de máquinas.', 'Serve apenas para alimentar a família do agricultor.', 'Alta produção voltada para exportação.', 'Produção feita apenas em quintais.']
        },
        {
            'pergunta': 'O que significa Monocultura?',
            'resposta': 'A produção de apenas uma especialidade agrícola.',
            'opcoes': ['Plantar muitos tipos diferentes de frutas.', 'A produção de apenas uma especialidade agrícola.', 'Retirar metais da natureza.', 'Criar vários tipos de animais juntos.']
        },
        {
            'pergunta': 'No período colonial, o Brasil era dependente da monocultura de qual produto?',
            'resposta': 'Cana-de-açúcar',
            'opcoes': ['Café', 'Soja', 'Cana-de-açúcar', 'Laranja']
        },
        {
            'pergunta': 'Qual destas opções é um insumo agrícola?',
            'resposta': 'Adubos, sementes e tratores.',
            'opcoes': ['Adubos, sementes e tratores.', 'Televisão e computador.', 'Ouro e prata.', 'Madeira e látex.']
        },
        {
            'pergunta': 'Em qual região do Brasil ficam localizados os Estados do Rio de Janeiro, São Paulo e Minas Gerais?',
            'resposta': 'Região Sudeste',
            'opcoes': ['Região Sul', 'Região Nordeste', 'Região Sudeste', 'Região Norte']
        },
        {
            'pergunta': 'Em qual região do Brasil fica o Estado do Amazonas?',
            'resposta': 'Região Norte',
            'opcoes': ['Região Sul', 'Região Centro-Oeste', 'Região Norte', 'Região Nordeste']
        },
        {
            'pergunta': 'Os Estados do Ceará, Bahia e Pernambuco ficam em qual região brasileira?',
            'resposta': 'Região Nordeste',
            'opcoes': ['Região Sul', 'Região Sudeste', 'Região Centro-Oeste', 'Região Nordeste']
        },
        {
            'pergunta': 'Paraná, Santa Catarina e Rio Grande do Sul são estados de qual região?',
            'resposta': 'Região Sul',
            'opcoes': ['Região Sul', 'Região Norte', 'Região Nordeste', 'Região Centro-Oeste']
        },
        {
            'pergunta': 'O Estado de Mato Grosso fica localizado em qual região do Brasil?',
            'resposta': 'Região Centro-Oeste',
            'opcoes': ['Região Sudeste', 'Região Centro-Oeste', 'Região Norte', 'Região Sul']
        },
        {
            'pergunta': 'Sobre os recursos naturais, marque a atitude CORRETA para preservar a natureza:',
            'resposta': 'Fechar a torneira enquanto escova os dentes.',
            'opcoes': ['Deixar a torneira aberta ao escovar os dentes.', 'Cortar todas as árvores e não plantar nenhuma.', 'Fechar a torneira enquanto escova os dentes.', 'Desperdiçar água limpa lavando a calçada.']
        },
        {
            'pergunta': 'Qual destas afirmações sobre o meio ambiente é FALSA (Incorreta)?',
            'resposta': 'O desmatamento é uma prática boa para o meio ambiente.',
            'opcoes': ['Devemos plantar novas árvores ao retirar madeira.', 'O desmatamento é uma prática boa para o meio ambiente.', 'A água é um recurso que não deve ser desperdiçado.', 'Precisamos cuidar da natureza para os tesouros não acabarem.']
        }
    ]
    itens_jogo = random.sample(banco_questoes, min(10, len(banco_questoes)))
    for q in itens_jogo:
        random.shuffle(q['opcoes'])
    contexto = {'questoes_json': json.dumps(itens_jogo)}
    return render(request, 'geografia_quiz.html', contexto)

@login_required(login_url='/')
def geografia_extrativismo(request):
    return render(request, 'geografia_extrativismo.html')

@login_required(login_url='/')
def geografia_pecuaria(request):
    distratores = ['confinamento', 'extensiva', 'ovino', 'suíno', 'equino', 'intensiva', 'aves', 'queijo', 'bovino', 'caprino', 'lã', 'soltos', 'pasto', 'computadores']
    templates = [
        {'frase': 'A pecuária ______ cria os animais soltos em fazendas com terrenos muito grandes.', 'resposta': 'extensiva'},
        {'frase': 'Na pecuária intensiva, os animais vivem em espaços menores chamados de ______.', 'resposta': 'confinamento'},
        {'frase': 'O rebanho ______ é formado pela criação de ovelhas e carneiros.', 'resposta': 'ovino'},
        {'frase': 'O rebanho ______ é composto pela criação de porcos.', 'resposta': 'suíno'},
        {'frase': 'Cavalos e éguas fazem parte da criação de gado ______.', 'resposta': 'equino'},
        {'frase': 'Na pecuária ______, o fazendeiro usa muita tecnologia, computadores, rações especiais e vacinas.', 'resposta': 'intensiva'},
        {'frase': 'A criação de ______ nos fornece produtos muito consumidos, como carne, ovos e penas.', 'resposta': 'aves'},
        {'frase': 'As vacas leiteiras nos fornecem leite, que é essencial na fabricação de manteiga e ______.', 'resposta': 'queijo'}
    ]
    
    moldes_escolhidos = random.sample(templates, min(6, len(templates)))
    frases_geradas = []
    
    for molde in moldes_escolhidos:
        resposta_certa = molde['resposta']
        opcoes_erradas = random.sample([d for d in distratores if d != resposta_certa], 3)
        opcoes_finais = opcoes_erradas + [resposta_certa]
        random.shuffle(opcoes_finais)
        frases_geradas.append({
            'frase': molde['frase'], 
            'resposta': resposta_certa, 
            'opcoes': opcoes_finais
        })
        
    contexto = {'frases_json': json.dumps(frases_geradas)}
    return render(request, 'geografia_pecuaria.html', contexto)

@login_required(login_url='/')
def geografia_espaco(request):
    return render(request, 'geografia_espaco.html')

@login_required(login_url='/')
def geografia_paisagem(request):
    banco_questoes = [
        {
            'pergunta': 'Qual é o nome do planeta em que vivemos?',
            'resposta': 'Terra',
            'opcoes': ['Marte', 'Saturno', 'Terra', 'Mercúrio']
        },
        {
            'pergunta': 'Ao olhar uma paisagem, o que encontramos no 1º Plano?',
            'resposta': 'Os elementos mais próximos da nossa visão.',
            'opcoes': ['O céu, as nuvens e as montanhas ao fundo.', 'Os elementos mais próximos da nossa visão.', 'Apenas fábricas e prédios altos.', 'Os animais que estão voando no céu.']
        },
        {
            'pergunta': 'O que costumamos ver no 3º Plano de uma paisagem?',
            'resposta': 'As coisas mais distantes, como o céu e montanhas ao fundo.',
            'opcoes': ['As pedras e o chão pertinho da gente.', 'As coisas mais distantes, como o céu e montanhas ao fundo.', 'As pessoas andando na nossa frente.', 'Os móveis de dentro de uma casa.']
        },
        {
            'pergunta': 'Qual é a visão quando observamos algo totalmente de cima para baixo (como um drone vendo o topo do telhado)?',
            'resposta': 'Visão Vertical',
            'opcoes': ['Visão Frontal', 'Visão Oblíqua', 'Visão Horizontal', 'Visão Vertical']
        },
        {
            'pergunta': 'Quais destes elementos da natureza podem alterar e modificar as paisagens (como furar rochas)?',
            'resposta': 'As chuvas, os ventos e o mar.',
            'opcoes': ['As pontes, as casas e os parques.', 'As fábricas e os prédios altos.', 'As chuvas, os ventos e o mar.', 'As ruas asfaltadas e os carros.']
        },
        {
            'pergunta': 'Se você observar uma casa de cima e de lado, conseguindo ver o telhado e a parte da frente ao mesmo tempo, que visão é essa?',
            'resposta': 'Visão Oblíqua',
            'opcoes': ['Visão Vertical', 'Visão Frontal', 'Visão Oblíqua', 'Visão Traseira']
        },
        {
            'pergunta': 'Se um aluno estiver parado no portão olhando diretamente para a porta de entrada da escola, qual visão ele terá?',
            'resposta': 'Visão Frontal',
            'opcoes': ['Visão Vertical', 'Visão Oblíqua', 'Visão Frontal', 'Visão Aérea']
        },
        {
            'pergunta': 'O calçadão, os prédios, as igrejas e as ruas asfaltadas são exemplos de quais elementos na paisagem?',
            'resposta': 'Elementos culturais (feitos pelas pessoas).',
            'opcoes': ['Elementos naturais (feitos pela natureza).', 'Elementos espaciais.', 'Elementos culturais (feitos pelas pessoas).', 'Elementos invisíveis.']
        },
        {
            'pergunta': 'Qual elemento da natureza é responsável por desgastar rochas na praia com a força das suas ondas ao longo do tempo?',
            'resposta': 'O mar.',
            'opcoes': ['O sol.', 'O mar.', 'As nuvens.', 'A vegetação.']
        }
    ]
    itens_jogo = random.sample(banco_questoes, min(8, len(banco_questoes)))
    for q in itens_jogo:
        random.shuffle(q['opcoes'])
    contexto = {'questoes_json': json.dumps(itens_jogo)}
    return render(request, 'geografia_paisagem.html', contexto)

# ─────────────────────────────────────────────
# SELETOR DE ANO
# ─────────────────────────────────────────────
@login_required(login_url='/')
def selecionar_ano(request):
    nome = request.user.first_name or request.user.username
    return render(request, 'selecionar_ano.html', {'nome': nome})


@login_required(login_url='/')
def definir_ano(request):
    ano = request.GET.get('ano', '3')
    anos_validos = ['1', '2', '3', '4', '5']
    if ano in anos_validos:
        request.session['ano_selecionado'] = ano
    return redirect('home')


# ─────────────────────────────────────────────
# MÓDULO DE HISTÓRIA
# ─────────────────────────────────────────────
@login_required(login_url='/')
def menu_historia(request):
    return render(request, 'menu_historia.html')


@login_required(login_url='/')
def historia_cidades(request):
    todas = list(
        BancoQuestao.objects.filter(disciplina__nome='historia', modulo='crescimento_cidades', ativo=True)
        .values('enunciado', 'resposta_correta', 'dados_extras', 'tipo')
    )
    banco = [
        {'pergunta': q['enunciado'], 'resposta': q['resposta_correta'], 'opcoes': q['dados_extras'].get('opcoes', [])}
        for q in todas if q['tipo'] == 'multipla_escolha'
    ]
    itens_jogo = random.sample(banco, min(10, len(banco)))
    for q in itens_jogo:
        random.shuffle(q['opcoes'])
    return render(request, 'historia_cidades.html', {'questoes_json': json.dumps(itens_jogo)})


@login_required(login_url='/')
def historia_municipio(request):
    todas = list(
        BancoQuestao.objects.filter(disciplina__nome='historia', modulo='municipio_cidadania', ativo=True)
        .values('enunciado', 'resposta_correta', 'dados_extras', 'tipo')
    )
    banco = [
        {'pergunta': q['enunciado'], 'resposta': q['resposta_correta'], 'opcoes': q['dados_extras'].get('opcoes', [])}
        for q in todas if q['tipo'] == 'multipla_escolha'
    ]
    itens_jogo = random.sample(banco, min(10, len(banco)))
    for q in itens_jogo:
        random.shuffle(q['opcoes'])
    return render(request, 'historia_municipio.html', {'questoes_json': json.dumps(itens_jogo)})
