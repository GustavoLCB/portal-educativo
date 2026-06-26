"""
populate_db.py
--------------
Execute na raiz do projeto (onde está o manage.py):
    python populate_db.py

Este script migra todas as questões que estavam no views.py
para o banco de dados, usando os models Disciplina e BancoQuestao.
Pode ser rodado mais de uma vez sem duplicar dados (usa get_or_create).
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from core.models import Disciplina, BancoQuestao

# ─────────────────────────────────────────────
# UTILITÁRIO
# ─────────────────────────────────────────────
def criar_questao(disciplina, modulo, tipo, enunciado, resposta, extras=None):
    obj, criado = BancoQuestao.objects.get_or_create(
        disciplina=disciplina,
        modulo=modulo,
        enunciado=enunciado,
        defaults={
            'tipo': tipo,
            'resposta_correta': resposta,
            'dados_extras': extras or {},
            'ativo': True,
        }
    )
    status = "✅ Criado" if criado else "⏭️  Já existe"
    print(f"  {status}: {enunciado[:60]}")
    return obj


# ─────────────────────────────────────────────
# DISCIPLINAS
# ─────────────────────────────────────────────
print("\n📚 Criando disciplinas...")
portugues, _ = Disciplina.objects.get_or_create(nome='portugues',  defaults={'nome_exibicao': 'Português'})
ingles,    _ = Disciplina.objects.get_or_create(nome='ingles',     defaults={'nome_exibicao': 'Inglês'})
geografia, _ = Disciplina.objects.get_or_create(nome='geografia',  defaults={'nome_exibicao': 'Geografia'})
print("  ✅ Português, Inglês e Geografia prontos.")


# ─────────────────────────────────────────────
# INGLÊS — VOCABULÁRIO
# ─────────────────────────────────────────────
print("\n🇬🇧 Populando: Inglês › Vocabulário...")
vocabulario = [
    {'palavra': 'Dog',        'emoji': '🐶'},
    {'palavra': 'Cat',        'emoji': '🐱'},
    {'palavra': 'Spider',     'emoji': '🕷️'},
    {'palavra': 'Mouse',      'emoji': '🐭'},
    {'palavra': 'Bird',       'emoji': '🐦'},
    {'palavra': 'Lion',       'emoji': '🦁'},
    {'palavra': 'Fish',       'emoji': '🐟'},
    {'palavra': 'Chicken',    'emoji': '🐔'},
    {'palavra': 'Elephant',   'emoji': '🐘'},
    {'palavra': 'School',     'emoji': '🏫'},
    {'palavra': 'Book',       'emoji': '📖'},
    {'palavra': 'Pencil',     'emoji': '✏️'},
    {'palavra': 'Computer',   'emoji': '💻'},
    {'palavra': 'Chair',      'emoji': '🪑'},
    {'palavra': 'Classroom',  'emoji': '🧑‍🏫'},
    {'palavra': 'Student',    'emoji': '🎒'},
    {'palavra': 'Earth',      'emoji': '🌍'},
    {'palavra': 'Sun',        'emoji': '☀️'},
    {'palavra': 'Moon',       'emoji': '🌙'},
    {'palavra': 'Rain',       'emoji': '🌧️'},
    {'palavra': 'Tree',       'emoji': '🌳'},
    {'palavra': 'River',      'emoji': '🏞️'},
    {'palavra': 'Fire',       'emoji': '🔥'},
    {'palavra': 'Snow',       'emoji': '❄️'},
    {'palavra': 'Wind',       'emoji': '🌬️'},
    {'palavra': 'Beach',      'emoji': '🏖️'},
    {'palavra': 'Car',        'emoji': '🚗'},
    {'palavra': 'Airplane',   'emoji': '✈️'},
    {'palavra': 'Bus',        'emoji': '🚌'},
    {'palavra': 'Building',   'emoji': '🏢'},
    {'palavra': 'Church',     'emoji': '⛪'},
    {'palavra': 'House',      'emoji': '🏠'},
    {'palavra': 'Door',       'emoji': '🚪'},
    {'palavra': 'Kitchen',    'emoji': '🍽️'},
    {'palavra': 'Bedroom',    'emoji': '🛏️'},
    {'palavra': 'Lamp',       'emoji': '💡'},
    {'palavra': 'Window',     'emoji': '🪟'},
    {'palavra': 'Umbrella',   'emoji': '☔'},
    {'palavra': 'Table',      'emoji': '/static/img/table.png', 'is_image': True},
    {'palavra': 'Orange',     'emoji': '🍊'},
    {'palavra': 'Apple',      'emoji': '🍎'},
    {'palavra': 'Potato',     'emoji': '🥔'},
    {'palavra': 'Banana',     'emoji': '🍌'},
    {'palavra': 'Pineapple',  'emoji': '🍍'},
    {'palavra': 'Onion',      'emoji': '🧅'},
    {'palavra': 'Tomato',     'emoji': '🍅'},
    {'palavra': 'Mango',      'emoji': '🥭'},
    {'palavra': 'Hat',        'emoji': '🎩'},
    {'palavra': 'Shorts',     'emoji': '🩳'},
    {'palavra': 'Shirt',      'emoji': '👕'},
    {'palavra': 'Pants',      'emoji': '👖'},
    {'palavra': 'Jacket',     'emoji': '🧥'},
    {'palavra': 'Shoes',      'emoji': '👞'},
    {'palavra': 'Foot',       'emoji': '🦶'},
    {'palavra': 'Feet',       'emoji': '👣'},
    {'palavra': 'Hand',       'emoji': '🖐️'},
    {'palavra': 'Eye',        'emoji': '👁️'},
    {'palavra': 'Head',       'emoji': '👤'},
    {'palavra': 'Hair',       'emoji': '💇'},
    {'palavra': 'Leg',        'emoji': '🦵'},
    {'palavra': 'Nose',       'emoji': '👃'},
    {'palavra': 'Mouth',      'emoji': '👄'},
    {'palavra': 'Ear',        'emoji': '👂'},
    {'palavra': 'Red',        'emoji': '🔴'},
    {'palavra': 'Blue',       'emoji': '🔵'},
    {'palavra': 'Happy',      'emoji': '😄'},
    {'palavra': 'Sad',        'emoji': '😢'},
    {'palavra': 'Play soccer','emoji': '⚽'},
    {'palavra': 'Ride a bike','emoji': '🚲'},
    {'palavra': 'Basketball', 'emoji': '🏀'},
    {'palavra': 'Chess game', 'emoji': '♟️'},
]
for item in vocabulario:
    criar_questao(ingles, 'vocabulario', 'vocabulario',
                  enunciado=item['palavra'],
                  resposta=item['palavra'],
                  extras={'emoji': item['emoji'], 'is_image': item.get('is_image', False)})


# ─────────────────────────────────────────────
# INGLÊS — COMPLETAR FRASES
# ─────────────────────────────────────────────
print("\n🇬🇧 Populando: Inglês › Completar Frases...")
ingles_frases = [
    {'frase': 'Do you have a pet ______?',              'variacoes': [{'resposta': 'dog', 'emoji': '🐶'}, {'resposta': 'cat', 'emoji': '🐱'}, {'resposta': 'mouse', 'emoji': '🐭'}, {'resposta': 'fish', 'emoji': '🐟'}]},
    {'frase': 'My favorite fruit is ______.',           'variacoes': [{'resposta': 'apple', 'emoji': '🍎'}, {'resposta': 'banana', 'emoji': '🍌'}, {'resposta': 'pineapple', 'emoji': '🍍'}, {'resposta': 'mango', 'emoji': '🥭'}, {'resposta': 'orange', 'emoji': '🍊'}]},
    {'frase': 'The book is on the ______.',             'variacoes': [{'resposta': 'table', 'emoji': '/static/img/table.png', 'is_image': True}]},
    {'frase': 'He likes to play ______.',               'variacoes': [{'resposta': 'soccer', 'emoji': '⚽'}, {'resposta': 'basketball', 'emoji': '🏀'}, {'resposta': 'chess', 'emoji': '♟️'}]},
    {'frase': 'Are you going to the ______?',           'variacoes': [{'resposta': 'beach', 'emoji': '🏖️'}, {'resposta': 'church', 'emoji': '⛪'}, {'resposta': 'house', 'emoji': '🏠'}, {'resposta': 'school', 'emoji': '🏫'}]},
    {'frase': 'I like to ______ in the park.',          'variacoes': [{'resposta': 'ride a bike', 'emoji': '🚲'}, {'resposta': 'play soccer', 'emoji': '⚽'}, {'resposta': 'swim', 'emoji': '🏊'}, {'resposta': 'rollerblade', 'emoji': '🛼'}]},
    {'frase': 'The color of the sky is ______.', 	    'variacoes': [{'resposta': 'blue', 'emoji': '☁️'}]},
    {'frase': 'The ______ is yellow.',                  'variacoes': [{'resposta': 'sun', 'emoji': '☀️'}, {'resposta': 'banana', 'emoji': '🍌'}]},
    {'frase': 'She is wearing a beautiful ______.', 	'variacoes': [{'resposta': 'shirt', 'emoji': '👕'}, {'resposta': 'jacket', 'emoji': '🧥'}, {'resposta': 'hat', 'emoji': '🎩'}]},
    {'frase': 'The weather today is ______.', 		    'variacoes': [{'resposta': 'sunny', 'emoji': '☀️'}, {'resposta': 'cloudy', 'emoji': '☁️'}, {'resposta': 'windy', 'emoji': '🌬️'}, {'resposta': 'rainy', 'emoji': '🌧️'}]},
    {'frase': 'I need a jacket because it is very ______!', 'variacoes': [{'resposta': 'cold', 'emoji': '🥶'}, {'resposta': 'windy', 'emoji': '🌬️'}]},
    {'frase': "Let's go to the beach! It is so ______ today.", 'variacoes': [{'resposta': 'hot', 'emoji': '🥵'}, {'resposta': 'warm', 'emoji': '😎'}, {'resposta': 'sunny', 'emoji': '☀️'}]},
]
for item in ingles_frases:
    criar_questao(ingles, 'frases', 'completar_frase',
                  enunciado=item['frase'],
                  resposta='(multiplas)',
                  extras={'variacoes': item['variacoes']})


# ─────────────────────────────────────────────
# PORTUGUÊS — ORTOGRAFIA
# ─────────────────────────────────────────────
print("\n🇧🇷 Populando: Português › Ortografia...")
ortografia = [
    {'palavra': 'CA___ORRO',       'resposta': 'CH', 'opcoes': ['X', 'CH', 'SH']},
    {'palavra': 'PÁ___ARO',        'resposta': 'SS', 'opcoes': ['S', 'SS', 'Ç']},
    {'palavra': 'E___ELENTE',      'resposta': 'XC', 'opcoes': ['C', 'S', 'XC']},
    {'palavra': 'A___ÚCAR',        'resposta': 'Ç',  'opcoes': ['S', 'SS', 'Ç']},
    {'palavra': 'GIRA___OL',       'resposta': 'SS', 'opcoes': ['S', 'SS', 'Ç']},
    {'palavra': '___INÁSTICA',     'resposta': 'G',  'opcoes': ['G', 'J']},
    {'palavra': 'MA___ESTADE',     'resposta': 'J',  'opcoes': ['G', 'J']},
    {'palavra': 'FA___INA',        'resposta': 'X',  'opcoes': ['X', 'CH', 'S']},
    {'palavra': 'CENOU___A',       'resposta': 'R',  'opcoes': ['R', 'RR']},
    {'palavra': 'CA___O (automóvel)', 'resposta': 'RR', 'opcoes': ['R', 'RR']},
    {'palavra': '___ACARÉ',        'resposta': 'J',  'opcoes': ['G', 'J']},
    {'palavra': '___ÍCARA',        'resposta': 'X',  'opcoes': ['X', 'CH', 'SS']},
]
for item in ortografia:
    criar_questao(portugues, 'ortografia', 'multipla_escolha',
                  enunciado=item['palavra'],
                  resposta=item['resposta'],
                  extras={'opcoes': item['opcoes']})


# ─────────────────────────────────────────────
# PORTUGUÊS — SÍLABA TÔNICA
# ─────────────────────────────────────────────
print("\n🇧🇷 Populando: Português › Sílaba Tônica...")
silabas_tonicas = [
    # Oxítonas
    {'palavra': 'CAFÉ',        'resposta': 'Oxítona'},
    {'palavra': 'AMOR',        'resposta': 'Oxítona'},
    {'palavra': 'PORTUGUÊS',   'resposta': 'Oxítona'},
    {'palavra': 'COMPUTADOR',  'resposta': 'Oxítona'},
    {'palavra': 'FELIZ',       'resposta': 'Oxítona'},
    {'palavra': 'FUTEBOL',     'resposta': 'Oxítona'},
    {'palavra': 'JACARÉ',      'resposta': 'Oxítona'},
    {'palavra': 'ANIMAL',      'resposta': 'Oxítona'},
    {'palavra': 'CORAÇÃO',     'resposta': 'Oxítona'},
    {'palavra': 'PAPEL',       'resposta': 'Oxítona'},
    {'palavra': 'INVESTIR',    'resposta': 'Oxítona'},
    {'palavra': 'JOGAR',       'resposta': 'Oxítona'},
    {'palavra': 'ABACAXI',     'resposta': 'Oxítona'},
    {'palavra': 'GIBI',        'resposta': 'Oxítona'},
    {'palavra': 'CHAPÉU',      'resposta': 'Oxítona'},
    # Paroxítonas
    {'palavra': 'MENINO',      'resposta': 'Paroxítona'},
    {'palavra': 'MESA',        'resposta': 'Paroxítona'},
    {'palavra': 'LÁPIS',       'resposta': 'Paroxítona'},
    {'palavra': 'FÁCIL',       'resposta': 'Paroxítona'},
    {'palavra': 'JANELA',      'resposta': 'Paroxítona'},
    {'palavra': 'LEGO',        'resposta': 'Paroxítona'},
    {'palavra': 'FERRARI',     'resposta': 'Paroxítona'},
    {'palavra': 'MERCEDES',    'resposta': 'Paroxítona'},
    {'palavra': 'CRAQUE',      'resposta': 'Paroxítona'},
    {'palavra': 'PRAIA',       'resposta': 'Paroxítona'},
    {'palavra': 'PRANCHA',     'resposta': 'Paroxítona'},
    {'palavra': 'PLANILHA',    'resposta': 'Paroxítona'},
    {'palavra': 'ESCOLINHA',   'resposta': 'Paroxítona'},
    {'palavra': 'TECLADO',     'resposta': 'Paroxítona'},
    {'palavra': 'CAVALEIRO',   'resposta': 'Paroxítona'},
    # Proparoxítonas
    {'palavra': 'MÁGICO',      'resposta': 'Proparoxítona'},
    {'palavra': 'ÁRVORE',      'resposta': 'Proparoxítona'},
    {'palavra': 'LÂMPADA',     'resposta': 'Proparoxítona'},
    {'palavra': 'PÁSSARO',     'resposta': 'Proparoxítona'},
    {'palavra': 'MÉDICO',      'resposta': 'Proparoxítona'},
    {'palavra': 'ESTATÍSTICA', 'resposta': 'Proparoxítona'},
    {'palavra': 'MÉXICO',      'resposta': 'Proparoxítona'},
    {'palavra': 'GRÁFICO',     'resposta': 'Proparoxítona'},
    {'palavra': 'MAURÍCIO',    'resposta': 'Proparoxítona'},
    {'palavra': 'MATEMÁTICA',  'resposta': 'Proparoxítona'},
    {'palavra': 'DÚVIDA',      'resposta': 'Proparoxítona'},
    {'palavra': 'ÍNDICE',      'resposta': 'Proparoxítona'},
    {'palavra': 'GINÁSTICA',   'resposta': 'Proparoxítona'},
    {'palavra': 'RÁPIDO',      'resposta': 'Proparoxítona'},
    {'palavra': 'RELÂMPAGO',   'resposta': 'Proparoxítona'},
    {'palavra': 'CÍRCULO',     'resposta': 'Proparoxítona'},
    {'palavra': 'BÚSSOLA',     'resposta': 'Proparoxítona'},
]
for item in silabas_tonicas:
    criar_questao(portugues, 'silaba_tonica', 'classificacao',
                  enunciado=item['palavra'],
                  resposta=item['resposta'])


# ─────────────────────────────────────────────
# PORTUGUÊS — SINÔNIMOS / ANTÔNIMOS
# ─────────────────────────────────────────────
print("\n🇧🇷 Populando: Português › Sinônimos/Antônimos...")
sinonimos = [
    {'palavra': 'RÁPIDO',   'oposto': 'LENTO'},
    {'palavra': 'QUENTE',   'oposto': 'FRIO'},
    {'palavra': 'LONGE',    'oposto': 'PERTO'},
    {'palavra': 'GRANDE',   'oposto': 'PEQUENO'},
    {'palavra': 'DIA',      'oposto': 'NOITE'},
    {'palavra': 'BOM',      'oposto': 'MAU'},
    {'palavra': 'CLARO',    'oposto': 'ESCURO'},
    {'palavra': 'CHEIO',    'oposto': 'VAZIO'},
    {'palavra': 'ALTO',     'oposto': 'BAIXO'},
    {'palavra': 'FORTE',    'oposto': 'FRACO'},
    {'palavra': 'FELIZ',    'oposto': 'TRISTE'},
    {'palavra': 'FÁCIL',    'oposto': 'DIFÍCIL'},
    {'palavra': 'GIGANTE',  'oposto': 'MINÚSCULO'},
    {'palavra': 'BARULHO',  'oposto': 'SILÊNCIO'},
    {'palavra': 'GORDO',    'oposto': 'MAGRO'},
    {'palavra': 'GROSSO',   'oposto': 'FINO'},
    {'palavra': 'BONITO',   'oposto': 'FEIO'},
    {'palavra': 'LIMPO',    'oposto': 'SUJO'},
]
for item in sinonimos:
    criar_questao(portugues, 'sinonimos', 'classificacao',
                  enunciado=item['palavra'],
                  resposta=item['oposto'],
                  extras={'par': item['oposto']})


# ─────────────────────────────────────────────
# PORTUGUÊS — CAÇADOR DE SÍLABAS
# ─────────────────────────────────────────────
print("\n🇧🇷 Populando: Português › Caçador de Sílabas...")
cacador_silabas = [
    {'palavra': 'SOL',          'separacao': 'SOL',              'resposta': 1},
    {'palavra': 'MAR',          'separacao': 'MAR',              'resposta': 1},
    {'palavra': 'GOL',          'separacao': 'GOL',              'resposta': 1},
    {'palavra': 'PAI',          'separacao': 'PAI',              'resposta': 1},
    {'palavra': 'LEGO',         'separacao': 'LE-GO',            'resposta': 2},
    {'palavra': 'CRAQUE',       'separacao': 'CRA-QUE',          'resposta': 2},
    {'palavra': 'PRAIA',        'separacao': 'PRAI-A',           'resposta': 2},
    {'palavra': 'CARRO',        'separacao': 'CAR-RO',           'resposta': 2},
    {'palavra': 'BOLA',         'separacao': 'BO-LA',            'resposta': 2},
    {'palavra': 'LIVRO',        'separacao': 'LI-VRO',           'resposta': 2},
    {'palavra': 'FERRARI',      'separacao': 'FER-RA-RI',        'resposta': 3},
    {'palavra': 'MERCEDES',     'separacao': 'MER-CE-DES',       'resposta': 3},
    {'palavra': 'FUTEBOL',      'separacao': 'FU-TE-BOL',        'resposta': 3},
    {'palavra': 'ESTAÇÃO',      'separacao': 'ES-TA-ÇÃO',        'resposta': 3},
    {'palavra': 'MÉXICO',       'separacao': 'MÉ-XI-CO',         'resposta': 3},
    {'palavra': 'PLANILHA',     'separacao': 'PLA-NI-LHA',       'resposta': 3},
    {'palavra': 'MOCHILA',      'separacao': 'MO-CHI-LA',        'resposta': 3},
    {'palavra': 'CELULAR',      'separacao': 'CE-LU-LAR',        'resposta': 3},
    {'palavra': 'ESCOLINHA',    'separacao': 'ES-CO-LI-NHA',     'resposta': 4},
    {'palavra': 'FILIPINAS',    'separacao': 'FI-LI-PI-NAS',     'resposta': 4},
    {'palavra': 'AVENTURA',     'separacao': 'A-VEN-TU-RA',      'resposta': 4},
    {'palavra': 'BRINCADEIRA',  'separacao': 'BRIN-CA-DEI-RA',   'resposta': 4},
    {'palavra': 'COMPUTADOR',   'separacao': 'COM-PU-TA-DOR',    'resposta': 4},
    {'palavra': 'ESTATÍSTICA',  'separacao': 'ES-TA-TÍS-TI-CA',  'resposta': 5},
    {'palavra': 'INVESTIMENTO', 'separacao': 'IN-VES-TI-MEN-TO', 'resposta': 5},
    {'palavra': 'MATEMÁTICA',   'separacao': 'MA-TE-MÁ-TI-CA',   'resposta': 5},
]
for item in cacador_silabas:
    criar_questao(portugues, 'silabas', 'classificacao',
                  enunciado=item['palavra'],
                  resposta=str(item['resposta']),
                  extras={'separacao': item['separacao'], 'num_silabas': item['resposta']})


# ─────────────────────────────────────────────
# PORTUGUÊS — DETETIVE DE PALAVRAS (GRAMÁTICA)
# ─────────────────────────────────────────────
print("\n🇧🇷 Populando: Português › Detetive de Palavras...")
gramatica = [
    {'pergunta': 'Na frase: "O peixe azul enfeita o aquário redondo.", quais palavras são os ADJETIVOS?',                                'resposta': 'azul e redondo',         'opcoes': ['peixe e aquário', 'azul e redondo', 'enfeita e redondo', 'O e azul']},
    {'pergunta': 'Na frase: "A geladeira branca estava cheia de comidas gostosas.", quais são os SUBSTANTIVOS COMUNS?',                  'resposta': 'geladeira e comidas',     'opcoes': ['branca e gostosas', 'estava e cheia', 'geladeira e comidas', 'A e de']},
    {'pergunta': 'Na frase: "Os meninos Gabriel e Lucas cuidam dos seus velhos brinquedos.", quais são os SUBSTANTIVOS PRÓPRIOS?',        'resposta': 'Gabriel e Lucas',         'opcoes': ['meninos e brinquedos', 'velhos e cuidam', 'Gabriel e Lucas', 'Os e dos']},
    {'pergunta': 'Na frase: "A mamãe Joana viu os passarinhos tristes na gaiola fria.", quais são os ADJETIVOS?',                        'resposta': 'tristes e fria',          'opcoes': ['mamãe e gaiola', 'Joana e passarinhos', 'tristes e fria', 'viu e na']},
    {'pergunta': 'Na frase: "Lucas montou um enorme carro da Ferrari.", quais são os SUBSTANTIVOS PRÓPRIOS?',                            'resposta': 'Lucas e Ferrari',         'opcoes': ['carro e enorme', 'Lucas e Ferrari', 'montou e um', 'enorme e carro']},
    {'pergunta': 'Na frase: "As belas praias do México têm águas cristalinas.", quais palavras são os ADJETIVOS?',                       'resposta': 'belas e cristalinas',     'opcoes': ['praias e águas', 'belas e cristalinas', 'México e águas', 'As e do']},
    {'pergunta': 'Na frase: "O menino corajoso pratica kitesurf no mar agitado.", quais são os SUBSTANTIVOS COMUNS?',                    'resposta': 'menino, kitesurf e mar',  'opcoes': ['corajoso e agitado', 'O e no', 'menino, kitesurf e mar', 'pratica e corajoso']},
    {'pergunta': 'Na frase: "A Mercedes prateada venceu a corrida difícil.", quais palavras são os ADJETIVOS?',                          'resposta': 'prateada e difícil',      'opcoes': ['Mercedes e corrida', 'venceu e a', 'prateada e difícil', 'prateada e corrida']},
    {'pergunta': 'Na frase: "A bola novinha rolou para o gol vazio.", quais são os SUBSTANTIVOS COMUNS?',                               'resposta': 'bola e gol',              'opcoes': ['novinha e vazio', 'rolou e para', 'bola e gol', 'A e o']},
    {'pergunta': 'Na frase: "O talentoso jogador marcou na Escolinha do bairro.", quais são os ADJETIVOS?',                             'resposta': 'talentoso',               'opcoes': ['jogador', 'Escolinha', 'bairro', 'talentoso']},
]
for item in gramatica:
    criar_questao(portugues, 'gramatica', 'multipla_escolha',
                  enunciado=item['pergunta'],
                  resposta=item['resposta'],
                  extras={'opcoes': item['opcoes']})


# ─────────────────────────────────────────────
# GEOGRAFIA — QUIZ GERAL
# ─────────────────────────────────────────────
print("\n🌎 Populando: Geografia › Quiz Geral...")
geo_quiz = [
    {'pergunta': 'O que é Agricultura Familiar (ou de Subsistência)?',                                          'resposta': 'Produção em pequenas propriedades feita por famílias.',      'opcoes': ['Produção apenas para exportar para outros países.', 'Produção em pequenas propriedades feita por famílias.', 'Plantação de apenas um tipo de alimento.', 'Criação de gado em fazendas gigantes.']},
    {'pergunta': 'Qual é a principal característica da Grande Agricultura Comercial?',                          'resposta': 'Alta produção voltada para exportação.',                        'opcoes': ['Produção feita sem o uso de máquinas.', 'Serve apenas para alimentar a família do agricultor.', 'Alta produção voltada para exportação.', 'Produção feita apenas em quintais.']},
    {'pergunta': 'O que significa Monocultura?',                                                                'resposta': 'A produção de apenas uma especialidade agrícola.',              'opcoes': ['Plantar muitos tipos diferentes de frutas.', 'A produção de apenas uma especialidade agrícola.', 'Retirar metais da natureza.', 'Criar vários tipos de animais juntos.']},
    {'pergunta': 'No período colonial, o Brasil era dependente da monocultura de qual produto?',                'resposta': 'Cana-de-açúcar',                                               'opcoes': ['Café', 'Soja', 'Cana-de-açúcar', 'Laranja']},
    {'pergunta': 'Qual destas opções é um insumo agrícola?',                                                    'resposta': 'Adubos, sementes e tratores.',                                  'opcoes': ['Adubos, sementes e tratores.', 'Televisão e computador.', 'Ouro e prata.', 'Madeira e látex.']},
    {'pergunta': 'Em qual região do Brasil ficam localizados os Estados do Rio de Janeiro, São Paulo e Minas Gerais?', 'resposta': 'Região Sudeste',                                        'opcoes': ['Região Sul', 'Região Nordeste', 'Região Sudeste', 'Região Norte']},
    {'pergunta': 'Em qual região do Brasil fica o Estado do Amazonas?',                                         'resposta': 'Região Norte',                                                 'opcoes': ['Região Sul', 'Região Centro-Oeste', 'Região Norte', 'Região Nordeste']},
    {'pergunta': 'Os Estados do Ceará, Bahia e Pernambuco ficam em qual região brasileira?',                    'resposta': 'Região Nordeste',                                              'opcoes': ['Região Sul', 'Região Sudeste', 'Região Centro-Oeste', 'Região Nordeste']},
    {'pergunta': 'Paraná, Santa Catarina e Rio Grande do Sul são estados de qual região?',                      'resposta': 'Região Sul',                                                   'opcoes': ['Região Sul', 'Região Norte', 'Região Nordeste', 'Região Centro-Oeste']},
    {'pergunta': 'O Estado de Mato Grosso fica localizado em qual região do Brasil?',                           'resposta': 'Região Centro-Oeste',                                          'opcoes': ['Região Sudeste', 'Região Centro-Oeste', 'Região Norte', 'Região Sul']},
    {'pergunta': 'Sobre os recursos naturais, marque a atitude CORRETA para preservar a natureza:',             'resposta': 'Fechar a torneira enquanto escova os dentes.',                  'opcoes': ['Deixar a torneira aberta ao escovar os dentes.', 'Cortar todas as árvores e não plantar nenhuma.', 'Fechar a torneira enquanto escova os dentes.', 'Desperdiçar água limpa lavando a calçada.']},
    {'pergunta': 'Qual destas afirmações sobre o meio ambiente é FALSA (Incorreta)?',                           'resposta': 'O desmatamento é uma prática boa para o meio ambiente.',         'opcoes': ['Devemos plantar novas árvores ao retirar madeira.', 'O desmatamento é uma prática boa para o meio ambiente.', 'A água é um recurso que não deve ser desperdiçado.', 'Precisamos cuidar da natureza para os tesouros não acabarem.']},
]
for item in geo_quiz:
    criar_questao(geografia, 'quiz', 'multipla_escolha',
                  enunciado=item['pergunta'],
                  resposta=item['resposta'],
                  extras={'opcoes': item['opcoes']})


# ─────────────────────────────────────────────
# GEOGRAFIA — PECUÁRIA (COMPLETAR FRASES)
# ─────────────────────────────────────────────
print("\n🌎 Populando: Geografia › Pecuária...")
geo_pecuaria = [
    {'frase': 'A pecuária ______ cria os animais soltos em fazendas com terrenos muito grandes.',               'resposta': 'extensiva'},
    {'frase': 'Na pecuária intensiva, os animais vivem em espaços menores chamados de ______.',                 'resposta': 'confinamento'},
    {'frase': 'O rebanho ______ é formado pela criação de ovelhas e carneiros.',                                'resposta': 'ovino'},
    {'frase': 'O rebanho ______ é composto pela criação de porcos.',                                            'resposta': 'suíno'},
    {'frase': 'Cavalos e éguas fazem parte da criação de gado ______.',                                         'resposta': 'equino'},
    {'frase': 'Na pecuária ______, o fazendeiro usa muita tecnologia, computadores, rações especiais e vacinas.','resposta': 'intensiva'},
    {'frase': 'A criação de ______ nos fornece produtos muito consumidos, como carne, ovos e penas.',           'resposta': 'aves'},
    {'frase': 'As vacas leiteiras nos fornecem leite, que é essencial na fabricação de manteiga e ______.',     'resposta': 'queijo'},
]
distratores_pecuaria = ['confinamento', 'extensiva', 'ovino', 'suíno', 'equino', 'intensiva', 'aves', 'queijo', 'bovino', 'caprino', 'lã', 'soltos', 'pasto', 'computadores']
for item in geo_pecuaria:
    criar_questao(geografia, 'pecuaria', 'completar_frase',
                  enunciado=item['frase'],
                  resposta=item['resposta'],
                  extras={'distratores': distratores_pecuaria})


# ─────────────────────────────────────────────
# GEOGRAFIA — PAISAGEM
# ─────────────────────────────────────────────
print("\n🌎 Populando: Geografia › Paisagem...")
geo_paisagem = [
    {'pergunta': 'Qual é o nome do planeta em que vivemos?',                                                                                                                    'resposta': 'Terra',                                              'opcoes': ['Marte', 'Saturno', 'Terra', 'Mercúrio']},
    {'pergunta': 'Ao olhar uma paisagem, o que encontramos no 1º Plano?',                                                                                                       'resposta': 'Os elementos mais próximos da nossa visão.',          'opcoes': ['O céu, as nuvens e as montanhas ao fundo.', 'Os elementos mais próximos da nossa visão.', 'Apenas fábricas e prédios altos.', 'Os animais que estão voando no céu.']},
    {'pergunta': 'O que costumamos ver no 3º Plano de uma paisagem?',                                                                                                           'resposta': 'As coisas mais distantes, como o céu e montanhas ao fundo.', 'opcoes': ['As pedras e o chão pertinho da gente.', 'As coisas mais distantes, como o céu e montanhas ao fundo.', 'As pessoas andando na nossa frente.', 'Os móveis de dentro de uma casa.']},
    {'pergunta': 'Qual é a visão quando observamos algo totalmente de cima para baixo (como um drone vendo o topo do telhado)?',                                                 'resposta': 'Visão Vertical',                                     'opcoes': ['Visão Frontal', 'Visão Oblíqua', 'Visão Horizontal', 'Visão Vertical']},
    {'pergunta': 'Quais destes elementos da natureza podem alterar e modificar as paisagens (como furar rochas)?',                                                              'resposta': 'As chuvas, os ventos e o mar.',                       'opcoes': ['As pontes, as casas e os parques.', 'As fábricas e os prédios altos.', 'As chuvas, os ventos e o mar.', 'As ruas asfaltadas e os carros.']},
    {'pergunta': 'Se você observar uma casa de cima e de lado, conseguindo ver o telhado e a parte da frente ao mesmo tempo, que visão é essa?',                                'resposta': 'Visão Oblíqua',                                      'opcoes': ['Visão Vertical', 'Visão Frontal', 'Visão Oblíqua', 'Visão Traseira']},
    {'pergunta': 'Se um aluno estiver parado no portão olhando diretamente para a porta de entrada da escola, qual visão ele terá?',                                            'resposta': 'Visão Frontal',                                      'opcoes': ['Visão Vertical', 'Visão Oblíqua', 'Visão Frontal', 'Visão Aérea']},
    {'pergunta': 'O calçadão, os prédios, as igrejas e as ruas asfaltadas são exemplos de quais elementos na paisagem?',                                                       'resposta': 'Elementos culturais (feitos pelas pessoas).',         'opcoes': ['Elementos naturais (feitos pela natureza).', 'Elementos espaciais.', 'Elementos culturais (feitos pelas pessoas).', 'Elementos invisíveis.']},
    {'pergunta': 'Qual elemento da natureza é responsável por desgastar rochas na praia com a força das suas ondas ao longo do tempo?',                                        'resposta': 'O mar.',                                             'opcoes': ['O sol.', 'O mar.', 'As nuvens.', 'A vegetação.']},
]
for item in geo_paisagem:
    criar_questao(geografia, 'paisagem', 'multipla_escolha',
                  enunciado=item['pergunta'],
                  resposta=item['resposta'],
                  extras={'opcoes': item['opcoes']})


# ─────────────────────────────────────────────
# RESUMO FINAL
# ─────────────────────────────────────────────
print("\n" + "="*50)
print("✅ POPULAÇÃO DO BANCO CONCLUÍDA!")
print("="*50)
total = BancoQuestao.objects.count()
print(f"\n📊 Total de questões no banco: {total}")
print(f"   🇧🇷 Português : {BancoQuestao.objects.filter(disciplina=portugues).count()}")
print(f"   🇬🇧 Inglês    : {BancoQuestao.objects.filter(disciplina=ingles).count()}")
print(f"   🌎 Geografia  : {BancoQuestao.objects.filter(disciplina=geografia).count()}")
print("\n💡 Próximo passo: adapte o views.py para buscar do banco.")
print("   Execute: python manage.py runserver")