from django.db import models
from django.contrib.auth.models import User

class RegistroJogada(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    operacao = models.CharField(max_length=50, default='multiplicacao')
    nivel = models.CharField(max_length=50, default='unidades')
    
    numero_1 = models.IntegerField(default=0)
    numero_2 = models.IntegerField(default=0)
    resposta_aluno = models.CharField(max_length=200, default='0')
    acertou = models.BooleanField()
    tempo_segundos = models.FloatField()
    data_jogada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        resultado = "Acertou" if self.acertou else "Errou"
        return f"{self.operacao} ({self.nivel}): {self.numero_1} e {self.numero_2} | Resp: {self.resposta_aluno} ({resultado})"

class Disciplina(models.Model):
    nome = models.CharField(max_length=50)
    nome_exibicao = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_exibicao

class BancoQuestao(models.Model):
    TIPOS = [
        ('multipla_escolha', 'Múltipla Escolha'),
        ('completar_frase', 'Completar Frase'),
        ('vocabulario', 'Vocabulário'),
        ('classificacao', 'Classificação'),
    ]
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    modulo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=30, choices=TIPOS)
    enunciado = models.TextField()
    resposta_correta = models.CharField(max_length=200)
    dados_extras = models.JSONField(default=dict, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.disciplina}][{self.modulo}] {self.enunciado[:50]}"
