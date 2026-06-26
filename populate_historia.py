"""
populate_historia.py
--------------------
Execute na raiz do projeto:
    python populate_historia.py

Popula o banco com questões de História — Capítulos 5 e 6
Colégio Santo Agostinho — 3º ano — 2º período 2026
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from core.models import Disciplina, BancoQuestao

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
    print(f"  {status}: {enunciado[:70]}")
    return obj


# ── DISCIPLINA ─────────────────────────────────────────────────────────────
print("\n📚 Criando disciplina História...")
historia, _ = Disciplina.objects.get_or_create(
    nome='historia',
    defaults={'nome_exibicao': 'História'}
)
print("  ✅ História pronta.")


# ══════════════════════════════════════════════════════════════════════════
# MÓDULO 1 — CRESCIMENTO DAS CIDADES (Capítulo 5)
# ══════════════════════════════════════════════════════════════════════════
print("\n🏙️  Populando: História › Crescimento das Cidades...")

# ── MÚLTIPLA ESCOLHA ──────────────────────────────────────────────────────
multipla_escolha_cidades = [
    {
        'enunciado': 'Como eram chamados os escravizados que trabalhavam nas ruas das cidades antigas, prestando serviços e vendendo produtos?',
        'resposta': 'Escravizados de ganho.',
        'opcoes': ['Escravizados de ouro.', 'Escravizados de corte.', 'Escravizados de ganho.', 'Escravizados domésticos.']
    },
    {
        'enunciado': 'Como era o comércio nas primeiras cidades brasileiras?',
        'resposta': 'Feito por vendedores ambulantes nas ruas.',
        'opcoes': ['Igual ao comércio atual, com shoppings e grandes mercados.', 'Só se vendiam frutas e legumes.', 'Feito por vendedores ambulantes nas ruas.', 'Só existiam lojas grandes.']
    },
    {
        'enunciado': 'Quando as cidades começaram a crescer por causa das indústrias, quem investiu dinheiro nas fábricas?',
        'resposta': 'Fazendeiros, com o dinheiro do café.',
        'opcoes': ['Músicos, com o dinheiro de shows.', 'Governantes, com o dinheiro dos impostos.', 'Fazendeiros, com o dinheiro do café.', 'Escritores, com a venda de livros.']
    },
    {
        'enunciado': 'O que são os cortiços?',
        'resposta': 'Moradias simples e apertadas com pouca estrutura.',
        'opcoes': ['Casas grandes com piscina.', 'Conjuntos de apartamentos de luxo.', 'Moradias simples e apertadas com pouca estrutura.', 'Hotéis para turistas.']
    },
    {
        'enunciado': 'O que tinham de especial as vilas operárias?',
        'resposta': 'Foram construídas pelas empresas para que os trabalhadores morassem perto das fábricas.',
        'opcoes': ['Eram muito distantes das fábricas.', 'Foram construídas pelos próprios trabalhadores.', 'Foram construídas pelas empresas para que os trabalhadores morassem perto das fábricas.', 'Eram casas muito diferentes umas das outras.']
    },
    {
        'enunciado': 'Qual foi o primeiro meio de transporte urbano coletivo nas cidades brasileiras?',
        'resposta': 'Bonde puxado por cavalos.',
        'opcoes': ['Ônibus.', 'Metrô.', 'Bonde puxado por cavalos.', 'Bonde elétrico.']
    },
    {
        'enunciado': 'A partir de 1950, o que substituiu os bondes em muitas cidades brasileiras?',
        'resposta': 'Os ônibus.',
        'opcoes': ['O metrô.', 'Os ônibus.', 'Os cavalos.', 'As bicicletas.']
    },
    {
        'enunciado': 'Qual produto gerou a riqueza que os fazendeiros investiram nas indústrias das cidades?',
        'resposta': 'O café.',
        'opcoes': ['A cana-de-açúcar.', 'O algodão.', 'O café.', 'A soja.']
    },
    {
        'enunciado': 'O que as fábricas das cidades produziam há mais de um século?',
        'resposta': 'Tecidos, roupas, calçados e alimentos como farinha, massas, doces e queijos.',
        'opcoes': ['Apenas carros e aviões.', 'Tecidos, roupas, calçados e alimentos como farinha, massas, doces e queijos.', 'Somente produtos eletrônicos.', 'Apenas móveis e utensílios domésticos.']
    },
    {
        'enunciado': 'O que aconteceu com os preços das casas quando muitas pessoas foram para as cidades trabalhar nas fábricas?',
        'resposta': 'Os preços subiram muito, causando falta de moradia.',
        'opcoes': ['Os preços caíram, pois havia muitas casas.', 'Os preços ficaram iguais.', 'Os preços subiram muito, causando falta de moradia.', 'O governo deu casas de graça para todos.']
    },
    {
        'enunciado': 'Qual das cidades abaixo foi um dos principais destinos do investimento dos fazendeiros de café nas indústrias?',
        'resposta': 'São Paulo.',
        'opcoes': ['Salvador.', 'Fortaleza.', 'São Paulo.', 'Manaus.']
    },
    {
        'enunciado': 'Como se chama o deslocamento de pessoas do campo para as cidades em busca de trabalho nas fábricas?',
        'resposta': 'Êxodo rural.',
        'opcoes': ['Migração marítima.', 'Êxodo rural.', 'Expansão urbana.', 'Colonização.']
    },
]

for q in multipla_escolha_cidades:
    criar_questao(
        historia, 'crescimento_cidades', 'multipla_escolha',
        enunciado=q['enunciado'],
        resposta=q['resposta'],
        extras={'opcoes': q['opcoes']}
    )

# ── COMPLETAR FRASES ───────────────────────────────────────────────────────
completar_cidades = [
    {'frase': 'Muitas pessoas saíram do ______ para trabalhar nas fábricas das cidades.',     'resposta': 'campo'},
    {'frase': 'As pessoas que saíram do campo foram para a ______ em busca de emprego.',       'resposta': 'cidade'},
    {'frase': 'Os ______ puxados por cavalos foram os primeiros meios de transporte coletivo.','resposta': 'bondes'},
    {'frase': 'Com o crescimento das cidades, surgiram moradias coletivas chamadas ______.',   'resposta': 'cortiços'},
    {'frase': 'As vilas ______ eram conjuntos de casas construídas perto das fábricas.',       'resposta': 'operárias'},
    {'frase': 'Os fazendeiros investiram nas cidades o dinheiro da produção de ______.',       'resposta': 'café'},
    {'frase': 'As fábricas produziam tecidos, calçados e alimentos como farinha e ______.',    'resposta': 'massas'},
    {'frase': 'As primeiras cidades brasileiras tinham vendedores ______ que vendiam nas ruas.','resposta': 'ambulantes'},
    {'frase': 'Os escravizados de ganho precisavam entregar a maior parte do dinheiro aos seus ______.',  'resposta': 'donos'},
    {'frase': 'Com as fábricas, o preço dos imóveis subiu e surgiu uma grave falta de ______.',          'resposta': 'moradia'},
]

distratores_cidades = ['campo', 'cidade', 'bondes', 'cortiços', 'operárias', 'café',
                       'massas', 'ambulantes', 'donos', 'moradia', 'metrô', 'ônibus',
                       'trabalho', 'casas', 'fazendeiros']

for q in completar_cidades:
    criar_questao(
        historia, 'crescimento_cidades', 'completar_frase',
        enunciado=q['frase'],
        resposta=q['resposta'],
        extras={'distratores': distratores_cidades}
    )


# ══════════════════════════════════════════════════════════════════════════
# MÓDULO 2 — O MUNICÍPIO É DE TODOS / CIDADANIA (Capítulo 6)
# ══════════════════════════════════════════════════════════════════════════
print("\n🏛️  Populando: História › O Município é de Todos...")

# ── MÚLTIPLA ESCOLHA ──────────────────────────────────────────────────────
multipla_escolha_municipio = [
    {
        'enunciado': 'Como é chamado o conjunto de leis brasileiras que define os direitos e deveres de todos os cidadãos?',
        'resposta': 'Constituição.',
        'opcoes': ['Código Civil.', 'Constituição.', 'Lei Municipal.', 'Decreto Federal.']
    },
    {
        'enunciado': 'Em que ano foi criada a Constituição Brasileira, conhecida como Constituição Cidadã?',
        'resposta': '1988.',
        'opcoes': ['1822.', '1945.', '1988.', '2000.']
    },
    {
        'enunciado': 'Qual das alternativas abaixo é um DIREITO do cidadão brasileiro segundo a Constituição?',
        'resposta': 'Saúde pública de qualidade.',
        'opcoes': ['Respeitar as leis do país.', 'Cuidar do meio ambiente.', 'Saúde pública de qualidade.', 'Respeitar as diferenças entre as pessoas.']
    },
    {
        'enunciado': 'Qual das alternativas abaixo é um DEVER do cidadão brasileiro segundo a Constituição?',
        'resposta': 'Cuidar do meio ambiente.',
        'opcoes': ['Ter moradia digna.', 'Cuidar do meio ambiente.', 'Ter educação gratuita.', 'Votar e ser votado.']
    },
    {
        'enunciado': 'O que são as ONGs?',
        'resposta': 'Organizações que defendem direitos das pessoas, da natureza e promovem saúde, moradia e educação.',
        'opcoes': ['Órgãos do governo federal.', 'Organizações que defendem direitos das pessoas, da natureza e promovem saúde, moradia e educação.', 'Empresas que vendem produtos nas cidades.', 'Grupos que organizam festas no bairro.']
    },
    {
        'enunciado': 'O que são os mutirões?',
        'resposta': 'Ações em grupo para pintar escolas, limpar praças e melhorar espaços públicos.',
        'opcoes': ['Reuniões do governo para criar leis.', 'Ações em grupo para pintar escolas, limpar praças e melhorar espaços públicos.', 'Empresas que constroem casas populares.', 'Festas organizadas pela prefeitura.']
    },
    {
        'enunciado': 'O que são as Associações de Moradores?',
        'resposta': 'Pessoas do mesmo bairro que se unem para buscar soluções para os problemas locais.',
        'opcoes': ['Grupos de empresários que investem no bairro.', 'Funcionários da prefeitura que cuidam das ruas.', 'Pessoas do mesmo bairro que se unem para buscar soluções para os problemas locais.', 'Clubes esportivos do município.']
    },
    {
        'enunciado': 'Mesmo sendo criança, como você pode praticar a cidadania no dia a dia?',
        'resposta': 'Jogando o lixo no lugar certo, ajudando quem precisa e respeitando professores e colegas.',
        'opcoes': ['Só votando nas eleições.', 'Apenas pagando impostos.', 'Jogando o lixo no lugar certo, ajudando quem precisa e respeitando professores e colegas.', 'Somente obedecendo às leis federais.']
    },
    {
        'enunciado': 'Depois de 1950, as cidades cresceram rapidamente. Qual foi o principal problema causado por esse crescimento rápido?',
        'resposta': 'Falta de casas, escolas, hospitais e transporte.',
        'opcoes': ['Excesso de parques e áreas verdes.', 'Falta de casas, escolas, hospitais e transporte.', 'Muitas pessoas querendo sair das cidades.', 'Sobra de empregos para todos.']
    },
    {
        'enunciado': 'Qual é o papel do governo em relação aos direitos dos cidadãos, segundo a Constituição?',
        'resposta': 'O governo tem a obrigação de garantir os direitos dos cidadãos.',
        'opcoes': ['O governo pode escolher quais direitos vai garantir.', 'O governo tem a obrigação de garantir os direitos dos cidadãos.', 'Somente os ricos têm direitos garantidos.', 'Os direitos só valem para os adultos.']
    },
    {
        'enunciado': 'A palavra "cidadania" está ligada à ideia de:',
        'resposta': 'Viver junto com outras pessoas, seguindo regras e ajudando a melhorar a vida de todos.',
        'opcoes': ['Morar em uma grande cidade.', 'Viver junto com outras pessoas, seguindo regras e ajudando a melhorar a vida de todos.', 'Ter muito dinheiro e poder.', 'Obedecer apenas as leis que você concorda.']
    },
    {
        'enunciado': 'Qual das alternativas abaixo NÃO é um bom exemplo de cidadania?',
        'resposta': 'Jogar lixo na rua.',
        'opcoes': ['Ajudar um colega com dificuldades.', 'Jogar lixo na rua.', 'Respeitar as regras da escola.', 'Cuidar dos espaços públicos do bairro.']
    },
]

for q in multipla_escolha_municipio:
    criar_questao(
        historia, 'municipio_cidadania', 'multipla_escolha',
        enunciado=q['enunciado'],
        resposta=q['resposta'],
        extras={'opcoes': q['opcoes']}
    )

# ── COMPLETAR FRASES ───────────────────────────────────────────────────────
completar_municipio = [
    {'frase': 'A palavra cidadania vem do latim e está ligada à ideia de viver ______ com outras pessoas.',  'resposta': 'junto'},
    {'frase': 'No Brasil, o conjunto de leis que define os direitos e deveres dos cidadãos é a ______.',     'resposta': 'Constituição'},
    {'frase': 'A Constituição Brasileira foi criada em ______ e é chamada de Constituição Cidadã.',          'resposta': '1988'},
    {'frase': 'Todo cidadão tem direito à ______, à educação e à moradia digna.',                            'resposta': 'saúde'},
    {'frase': 'Cuidar do meio ambiente é um ______ de todos os cidadãos.',                                  'resposta': 'dever'},
    {'frase': 'As pessoas do mesmo bairro que se unem para resolver problemas formam uma Associação de ______.',  'resposta': 'Moradores'},
    {'frase': 'Ações em grupo para limpar praças e pintar escolas são chamadas de ______.',                  'resposta': 'mutirões'},
    {'frase': 'Organizações que defendem direitos e promovem saúde e educação são chamadas de ______.',      'resposta': 'ONGs'},
    {'frase': 'Jogar o lixo no lugar certo e respeitar os colegas são atitudes de boa ______.',             'resposta': 'cidadania'},
    {'frase': 'Todos os cidadãos têm direitos, mas também têm ______ a cumprir.',                           'resposta': 'deveres'},
]

distratores_municipio = ['junto', 'Constituição', '1988', 'saúde', 'dever', 'Moradores',
                         'mutirões', 'ONGs', 'cidadania', 'deveres', 'direitos', 'voto',
                         'governo', 'escola', 'prefeitura', 'separados']

for q in completar_municipio:
    criar_questao(
        historia, 'municipio_cidadania', 'completar_frase',
        enunciado=q['frase'],
        resposta=q['resposta'],
        extras={'distratores': distratores_municipio}
    )


# ── RESUMO FINAL ───────────────────────────────────────────────────────────
print("\n" + "="*55)
print("✅ POPULAÇÃO DE HISTÓRIA CONCLUÍDA!")
print("="*55)
from core.models import BancoQuestao
total = BancoQuestao.objects.filter(disciplina=historia).count()
print(f"\n📊 Total de questões de História no banco: {total}")
print(f"   🏙️  Crescimento das Cidades  : {BancoQuestao.objects.filter(disciplina=historia, modulo='crescimento_cidades').count()}")
print(f"   🏛️  O Município é de Todos   : {BancoQuestao.objects.filter(disciplina=historia, modulo='municipio_cidadania').count()}")
print("\n💡 Próximo passo: criar as views, urls e templates de História.")
