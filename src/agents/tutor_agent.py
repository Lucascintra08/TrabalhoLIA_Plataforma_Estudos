# src/agents/tutor_agent.py
from src.services.gemini import chat_gemini


def _persona_tutor(nivel: str, materia: str) -> str:
    """
    Define uma persona simples de tutor, mas sem exagerar no 'modo professor'
    para não gerar textos muito longos.
    """
    return f"""
Você é um gerador de conteúdo para estudo de {materia} no nível {nivel}.
Seu objetivo é ser CLARO e OBJETIVO, sem enrolação.
"""


def gerar_resumo(
    texto: str,
    nivel: str = "Ensino Médio",
    materia: str = "Matemática",
) -> str:
    persona = _persona_tutor(nivel, materia)
    prompt = f"""
{persona}

A seguir há um texto de estudo. Gere um RESUMO organizado e COMPLETO em tópicos,
com foco em pontos importantes para prova de {materia} no nível {nivel}.

Regras:
- Escreva em português.
- Não repita o texto original.

Texto:
\"\"\"{texto}\"\"\"
"""
    return chat_gemini(prompt)


def gerar_questoes(
    texto: str,
    n_questoes: int = 5,
    nivel: str = "Ensino Médio",
    materia: str = "Matemática",
) -> str:
    """
    Gera questões de múltipla escolha em TEXTO CORRIDO.
    A página Tutor faz o pós-processamento para empilhar as alternativas.
    """
    persona = _persona_tutor(nivel, materia)
    prompt = f"""
{persona}

Gere {n_questoes} questões de múltipla escolha sobre {materia},
no nível {nivel}, baseadas EXCLUSIVAMENTE no texto abaixo.

FORMATO OBRIGATÓRIO (não coloque explicações, apenas questões e gabarito):

1) Enunciado da questão...
A) alternativa 1
B) alternativa 2
C) alternativa 3
D) alternativa 4

2) Enunciado da questão...
A) ...
B) ...
C) ...
D) ...

(continue até {n_questoes})

Ao final, escreva:

GABARITO:
1) A
2) C
3) D
...

NÃO:
- Explique as respostas.
- Dê aula.
- Faça comentários extras.
- Use markdown.

Texto base:
\"\"\"{texto}\"\"\"
"""
    return chat_gemini(prompt)
