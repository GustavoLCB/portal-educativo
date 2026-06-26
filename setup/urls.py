from django.contrib import admin
from django.urls import path
from core import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.login_view, name='login'), 
    path('sair/', views.logout_view, name='logout'), 
    path('cadastro/', views.registro_view, name='registro'), 
    
    path('home/', views.home, name='home'), 
    path('relatorio/', views.relatorio_desempenho, name='relatorio'), 
    
    path('matematica/', views.matematica, name='matematica'), 
    path('matematica/adicao/', views.niveis_adicao, name='niveis_adicao'), 
    path('matematica/subtracao/', views.niveis_subtracao, name='niveis_subtracao'), 
    path('matematica/multiplicacao/', views.niveis_multiplicacao, name='niveis_multiplicacao'), 
    path('matematica/divisao/', views.niveis_divisao, name='niveis_divisao'),
    path('matematica/potenciacao/', views.niveis_potenciacao, name='niveis_potenciacao'), 
    
    path('jogo/<str:operacao>/<str:nivel>/', views.jogo_tabuada, name='jogo_tabuada'), 
    path('salvar_jogada/', views.salvar_jogada, name='salvar_jogada'), 

    # --- MENUS DE NÍVEL 2 ---
    path('portugues/', views.menu_portugues, name='menu_portugues'),
    path('ingles/', views.menu_ingles, name='menu_ingles'),

    # --- MÓDULO DE INGLÊS ---
    path('ingles/vocabulario/', views.ingles_vocabulario, name='ingles_vocabulario'),
    path('ingles/frases/', views.ingles_frases, name='ingles_frases'),

    # --- MÓDULO DE PORTUGUÊS ---
    path('portugues/ortografia/', views.portugues_ortografia, name='portugues_ortografia'),
    path('portugues/silaba/', views.portugues_silaba, name='portugues_silaba'),
    path('portugues/sinonimos/', views.portugues_sinonimos, name='portugues_sinonimos'),
    path('portugues/silabas/', views.portugues_silabas, name='portugues_silabas'),
    path('portugues/gramatica/', views.portugues_gramatica, name='portugues_gramatica'),
    path('portugues/encontros/', views.portugues_encontros_vocalicos, name='portugues_encontros_vocalicos'),
    path('portugues/digrafo/', views.portugues_digrafo, name='portugues_digrafo'),
    
    # --- MÓDULO DE GEOGRAFIA ---
    path('geografia/', views.menu_geografia, name='menu_geografia'),
    path('geografia/mapa/', views.geografia_mapa, name='geografia_mapa'),
    path('geografia/quiz/', views.geografia_quiz, name='geografia_quiz'),
    path('geografia/extrativismo/', views.geografia_extrativismo, name='geografia_extrativismo'),
    path('geografia/pecuaria/', views.geografia_pecuaria, name='geografia_pecuaria'),
    path('geografia/espaco/', views.geografia_espaco, name='geografia_espaco'),
    path('geografia/paisagem/', views.geografia_paisagem, name='geografia_paisagem'),

    # --- SELETOR DE ANO ---
    path('selecionar-ano/', views.selecionar_ano, name='selecionar_ano'),
    path('definir-ano/', views.definir_ano, name='definir_ano'),

    # --- MÓDULO DE HISTÓRIA ---
    path('historia/', views.menu_historia, name='menu_historia'),
    path('historia/cidades/', views.historia_cidades, name='historia_cidades'),
    path('historia/municipio/', views.historia_municipio, name='historia_municipio'),
]