# src/agents/question_solver_agent.py
from typing import List, Optional
import json

from src.models import SolvedQuestion
from src.services.gemini import chat_gemini
from src.config import QUESTOES_FILE


def carregar_questoes_resolvidas() -> List[SolvedQuestion]:
    """Carrega a lista de questões resolvidas do arquivo JSON."""
    if QUESTOES_FILE.exists():
        data = json.loads(QUESTOES_FILE.read_text(encoding="utf-8"))
        return [SolvedQuestion.model_validate(q) for q in data]
    return []


def salvar_questoes(questoes: List[SolvedQuestion]) -> None:
    """Salva a lista de questões resolvidas no arquivo JSON."""
    QUESTOES_FILE.write_text(
        "[" + ",\n".join([q.model_dump_json(ensure_ascii=False) for q in questoes]) + "]",
        encoding="utf-8",
    )


def resolver_questao(
    enunciado: str,
    alternativas: Optional[str],
    resposta_aluno: Optional[str],
    materia: Optional[str],
    nivel: str,
    questoes_existentes: List[SolvedQuestion],
) -> tuple[str, List[SolvedQuestion]]:
    """
    Usa o Gemini para resolver e comentar uma questão,
    adaptando a explicação ao nível e à matéria.
    """
    prompt = f"""
Você é um professor de {materia or "matérias do ensino médio"} para alunos de {nivel}.

Enunciado da questão:
\"\"\"{enunciado}\"\"\"


Alternativas (se houver):
\"\"\"{alternativas or "Não há alternativas, é questão dissertativa."}\"\"\"


Resposta marcada pelo aluno (se informada): {resposta_aluno or "não informada"}
Matéria/tema (se informado): {materia or "não informado"}

Tarefas:
1. Diga claramente qual é a resposta correta (letra ou texto).
2. Explique passo a passo o raciocínio em linguagem adequada a {nivel}.
3. Justifique por que as alternativas erradas estão erradas (se existirem).
4. Dê uma dica de memorização ou macete em 1–2 frases.
5. Sugira uma tag de assunto (ex: "Funções do 1º grau",
   "Revolução Francesa", "Citologia", "Óptica geométrica", etc.)

Formate a resposta em markdown com as seções:

- **Gabarito**
- **Raciocínio comentado**
- **Análise das alternativas**
- **Dica de memorização**
- **Assunto / Tag**
"""
    texto = chat_gemini(prompt)

    registro = SolvedQuestion(
        enunciado=enunciado,
        alternativas=alternativas,
        resposta_aluno=resposta_aluno,
        materia=materia,
        correcao_markdown=texto,
    )

    questoes_novas = questoes_existentes + [registro]
    salvar_questoes(questoes_novas)

    return texto, questoes_novas
