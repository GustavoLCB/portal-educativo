# 📚 Tutorial: Como Inserir Novas Questões no PortalEdu

**Versão:** 1.0 | **Projeto:** PORTALEDU | **Atualizado em:** Junho 2026

---

## 📋 Índice

1. [Como funciona o sistema](#como-funciona)
2. [Matemática](#matematica)
3. [Português](#portugues)
4. [Inglês](#ingles)
5. [Geografia](#geografia)
6. [História (disciplina nova)](#historia)
7. [Checklist rápido](#checklist)

---

## 1. Como funciona o sistema {#como-funciona}

O PortalEdu tem **dois tipos de questões**:

| Tipo | Onde ficam | Como editar |
|---|---|---|
| **Banco de dados** | Tabela `BancoQuestao` | Django Admin |
| **JavaScript fixo** | Dentro do arquivo `.html` | VS Code |

### Quais matérias usam banco de dados?
- Português (Ortografia, Sílaba Tônica, Sinônimos, Caçador de Sílabas, Detetive de Palavras)
- Inglês (Vocabulário, Completar Frases)
- Geografia (Quiz Agricultura, Pecuária, Paisagens)

### Quais matérias usam JavaScript fixo?
- Português (Encontros Vocálicos, Dígrafos)
- Matemática (geração automática de números)

---

## 2. Matemática {#matematica}

A Matemática **gera os números automaticamente** — não há questões fixas para inserir. O que você pode configurar são os **níveis de dificuldade** e as **operações disponíveis**.

### Adicionar nova operação (ex: Potenciação)

**Passo 1** — Criar o template de níveis em `core/templates/`:
- Copie `niveis_multiplicacao.html`
- Renomeie para `niveis_potenciacao.html`
- Ajuste o título e os links internos

**Passo 2** — Adicionar a view em `core/views.py`:
```python
@login_required(login_url='/')
def niveis_potenciacao(request):
    return render(request, 'niveis_potenciacao.html')
```

**Passo 3** — Adicionar a rota em `setup/urls.py`:
```python
path('matematica/potenciacao/', views.niveis_potenciacao, name='niveis_potenciacao'),
```

**Passo 4** — Adicionar o card no template `matematica.html`:
```html
<a href="{% url 'niveis_potenciacao' %}" class="card card-potencias">
    <span class="titulo">Potenciação</span>
    <span class="icone">⚡</span>
</a>
```

**Passo 5** — Adicionar a lógica de geração no `jogo.html` dentro de `gerarNumerosInteligentes()`:
```javascript
} else if (operacaoAtual === 'potenciacao') {
    n1 = getRandom(2, 9);
    n2 = getRandom(2, 3);
    res = Math.pow(n1, n2);
    sinal = '^';
}
```

---

## 3. Português {#portugues}

### 3a. Matérias com banco de dados

Acesse `http://127.0.0.1:8000/admin` → **Banco de Questões** → **Adicionar**.

#### Ortografia (lacunas)
```
Disciplina:       Português
Módulo:           ortografia
Tipo:             multipla_escolha
Enunciado:        CA___BELO
Resposta correta: B
Dados extras:     {"opcoes": ["B", "V", "P"]}
```

#### Sílaba Tônica
```
Disciplina:       Português
Módulo:           silaba_tonica
Tipo:             classificacao
Enunciado:        ABACATE
Resposta correta: Paroxítona
Dados extras:     {}
```
> Resposta deve ser exatamente: `Oxítona`, `Paroxítona` ou `Proparoxítona`

#### Sinônimos / Antônimos
```
Disciplina:       Português
Módulo:           sinonimos
Tipo:             classificacao
Enunciado:        FRIO
Resposta correta: QUENTE
Dados extras:     {"par": "QUENTE"}
```

#### Caçador de Sílabas
```
Disciplina:       Português
Módulo:           silabas
Tipo:             classificacao
Enunciado:        BORBOLETA
Resposta correta: 4
Dados extras:     {"separacao": "BOR-BO-LE-TA", "num_silabas": 4}
```
> `resposta_correta` = número de sílabas (como texto: "1", "2", "3"...)

#### Detetive de Palavras (Gramática)
```
Disciplina:       Português
Módulo:           gramatica
Tipo:             multipla_escolha
Enunciado:        Na frase "O gato preto dorme.", quais são os ADJETIVOS?
Resposta correta: preto
Dados extras:     {"opcoes": ["gato", "preto", "dorme", "O"]}
```

---

### 3b. Matérias com JavaScript fixo

#### Encontros Vocálicos
Abra `core/templates/portugues_encontros_vocalicos.html` no VS Code.
Localize `const banco = [` e adicione novas linhas antes do `];`:

```javascript
{ palavra: 'TREINO',  resposta: 'Ditongo',  explicacao: 'TREI-NO → "EI" na mesma sílaba. <strong>Ditongo</strong>!' },
{ palavra: 'JUÍZO',   resposta: 'Hiato',    explicacao: 'JU-Í-ZO → "U" e "Í" separados. <strong>Hiato</strong>!' },
{ palavra: 'SAGUÃO',  resposta: 'Tritongo', explicacao: 'SA-GUÃO → "UÃO" juntos. <strong>Tritongo</strong>!' },
```
> `resposta` deve ser exatamente: `'Ditongo'`, `'Tritongo'` ou `'Hiato'`

#### Dígrafos
Abra `core/templates/portugues_digrafo.html` no VS Code.
Localize `const banco = [` e adicione antes do `];`:

```javascript
{ palavra: 'CHUCHU',  resposta: ['CH'], explicacao: '<strong>CH</strong>U-<strong>CH</strong>U → dígrafo CH aparece duas vezes!' },
{ palavra: 'TOALHA',  resposta: ['LH'], explicacao: 'TO-A-<strong>LH</strong>A → "LH" formam um único som. <strong>Dígrafo LH</strong>!' },
```
> `resposta` é sempre um array: `['CH']` para um dígrafo, `['SS', 'NH']` para dois

---

## 4. Inglês {#ingles}

### Vocabulário (Drag & Drop)
Acesse o Admin → **Banco de Questões** → **Adicionar**:
```
Disciplina:       Inglês
Módulo:           vocabulario
Tipo:             vocabulario
Enunciado:        Flower
Resposta correta: Flower
Dados extras:     {"emoji": "🌸", "is_image": false}
```
> Para usar imagem no lugar de emoji: `{"emoji": "/static/img/nome.png", "is_image": true}`

### Completar Frases
```
Disciplina:       Inglês
Módulo:           frases
Tipo:             completar_frase
Enunciado:        The cat is on the ______.
Resposta correta: (multiplas)
Dados extras:     {"variacoes": [
                    {"resposta": "chair", "emoji": "🪑"},
                    {"resposta": "table", "emoji": "🌸", "is_image": false}
                  ]}
```
> Cada variação é uma resposta possível para completar a frase

---

## 5. Geografia {#geografia}

### Quiz Agricultura / Quiz Paisagens (múltipla escolha)
```
Disciplina:       Geografia
Módulo:           quiz          ← para agricultura
Módulo:           paisagem      ← para paisagens
Tipo:             multipla_escolha
Enunciado:        O que é o Cerrado?
Resposta correta: Um bioma do Brasil Central com vegetação rasteira.
Dados extras:     {"opcoes": [
                    "Um bioma do Brasil Central com vegetação rasteira.",
                    "Uma floresta densa da Amazônia.",
                    "Uma região desértica do Nordeste.",
                    "Uma planície alagada do Pantanal."
                  ]}
```
> A `resposta_correta` deve ser **idêntica** a uma das opções em `dados_extras`

### Pecuária (completar frases)
```
Disciplina:       Geografia
Módulo:           pecuaria
Tipo:             completar_frase
Enunciado:        O rebanho ______ é composto por cabras e bodes.
Resposta correta: caprino
Dados extras:     {}
```
> Os distratores (opções erradas) são gerados automaticamente pela view

---

## 6. História (disciplina nova) {#historia}

Para criar a disciplina de História do zero, siga estes passos na ordem:

### Passo 1 — Criar a Disciplina no Admin
Acesse Admin → **Disciplinas** → **Adicionar**:
```
Nome:           historia
Nome exibição:  História
```

### Passo 2 — Cadastrar questões no Admin
Acesse Admin → **Banco de Questões** → **Adicionar**:
```
Disciplina:       História
Módulo:           brasil_colonial    ← nome livre, você escolhe
Tipo:             multipla_escolha
Enunciado:        Quem foi o primeiro governador-geral do Brasil?
Resposta correta: Tomé de Sousa
Dados extras:     {"opcoes": ["Tomé de Sousa", "Pedro Álvares Cabral", "Dom João III", "Duarte da Costa"]}
```

### Passo 3 — Criar a view em `core/views.py`
```python
@login_required(login_url='/')
def menu_historia(request):
    return render(request, 'menu_historia.html')

@login_required(login_url='/')
def historia_quiz(request):
    todas = list(
        BancoQuestao.objects.filter(disciplina__nome='historia', modulo='brasil_colonial', ativo=True)
        .values('enunciado', 'resposta_correta', 'dados_extras')
    )
    banco = [
        {
            'pergunta': q['enunciado'],
            'resposta': q['resposta_correta'],
            'opcoes': q['dados_extras'].get('opcoes', [])
        }
        for q in todas
    ]
    itens_jogo = random.sample(banco, min(8, len(banco)))
    for q in itens_jogo:
        random.shuffle(q['opcoes'])
    contexto = {'questoes_json': json.dumps(itens_jogo)}
    return render(request, 'historia_quiz.html', contexto)
```

### Passo 4 — Adicionar rotas em `setup/urls.py`
```python
path('historia/', views.menu_historia, name='menu_historia'),
path('historia/quiz/', views.historia_quiz, name='historia_quiz'),
```

### Passo 5 — Criar os templates
- Copie `menu_geografia.html` → renomeie para `menu_historia.html` → ajuste título e links
- Copie `geografia_quiz.html` → renomeie para `historia_quiz.html` → ajuste título

### Passo 6 — Adicionar card na home
Abra `home.html` e adicione o card de História no mesmo padrão dos outros.

---

## 7. Checklist rápido {#checklist}

Use este checklist sempre que criar algo novo:

### Adicionar questão em módulo existente
- [ ] Acessar Admin → Banco de Questões → Adicionar
- [ ] Preencher Disciplina, Módulo, Tipo, Enunciado, Resposta correta, Dados extras
- [ ] Salvar e testar no jogo

### Adicionar módulo novo em disciplina existente
- [ ] Cadastrar questões no Admin com o novo `modulo`
- [ ] Criar a view no `views.py`
- [ ] Adicionar a rota no `urls.py`
- [ ] Criar o template HTML (copiar um existente e adaptar)
- [ ] Adicionar o card no menu da disciplina

### Criar disciplina nova do zero
- [ ] Admin → Disciplinas → Adicionar
- [ ] Cadastrar questões no Admin
- [ ] Criar views (menu + cada módulo) no `views.py`
- [ ] Adicionar rotas no `urls.py`
- [ ] Criar templates (menu + cada módulo)
- [ ] Adicionar card na `home.html`
- [ ] Reiniciar o servidor: `python manage.py runserver`

---

## ⚠️ Regras importantes

1. **Nunca edite** o banco de dados diretamente — sempre use o Admin
2. **Resposta correta** deve ser **idêntica** a uma das opções nos `dados_extras`
3. Após qualquer mudança em `.py`, **reinicie o servidor**
4. Após mudança em `.html`, pressione **Ctrl+Shift+R** no navegador
5. O campo `modulo` no Admin deve bater **exatamente** com o nome usado na view

