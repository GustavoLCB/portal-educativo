from django.contrib import admin
from .models import RegistroJogada, Disciplina, BancoQuestao

# ── Registro de Jogadas (atualizado: agora mostra operação e nível na lista) ──
class RegistroJogadaAdmin(admin.ModelAdmin):
    list_display = ('operacao', 'nivel', 'numero_1', 'numero_2', 'resposta_aluno', 'acertou', 'tempo_segundos', 'data_jogada')
    list_filter = ('operacao', 'nivel', 'acertou')
    ordering = ('-data_jogada',)  # mais recentes primeiro, por padrão

admin.site.register(RegistroJogada, RegistroJogadaAdmin)


# ── Disciplinas ───────────────────────────────────────
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nome_exibicao')

admin.site.register(Disciplina, DisciplinaAdmin)


# ── Banco de Questões ─────────────────────────────────
class BancoQuestaoAdmin(admin.ModelAdmin):
    list_display  = ('disciplina', 'modulo', 'tipo', 'enunciado_curto', 'resposta_correta', 'ativo')
    list_filter   = ('disciplina', 'modulo', 'tipo', 'ativo')
    search_fields = ('enunciado', 'resposta_correta')
    list_editable = ('ativo',)

    def enunciado_curto(self, obj):
        return obj.enunciado[:60]
    enunciado_curto.short_description = 'Enunciado'

admin.site.register(BancoQuestao, BancoQuestaoAdmin)
