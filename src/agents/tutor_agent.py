# src/agents/tutor_agent.py
from src.services.gemini import chat_gemini


def _persona_tutor(nivel: str, materia: str) -> str:
    return f"""
Você é um professor de {materia} para alunos de {nivel}.
Explique de forma clara, didática, com exemplos simples,
sem pressupor conhecimento avançado.
"""


def gerar_resumo(texto: str, nivel: str = "Ensino Médio", materia: str = "Matemática") -> str:
    persona = _persona_tutor(nivel, materia)
    prompt = f"""
{persona}

Resuma o texto abaixo enfatizando:
- ideias principais
- definições importantes
- fórmulas ou palavras-chave (se houver)
- exemplos simples quando possível

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
    persona = _persona_tutor(nivel, materia)
    prompt = f"""
{persona}

Gere {n_questoes} questões de múltipla escolha de {materia},
no nível de {nivel}, baseadas APENAS no texto abaixo.

Regras:
- 4 alternativas (A, B, C, D), escreva as alternativas no formato:
    A) "alternativa 1"
    B) "alternativa 2"
    C) "alternativa 3"
    D) "alternativa 4"
- Apenas UMA correta
- Misture questões conceituais e de aplicação
- Evite questões absurdamente difíceis para {nivel}

Ao final, escreva o gabarito na forma:
1) A
2) C
3) D
...

Texto base:
\"\"\"{texto}\"\"\"
"""
    return chat_gemini(prompt)
