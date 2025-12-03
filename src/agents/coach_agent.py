# src/agents/coach_agent.py
import json
from src.models import StudyConfig, Progresso, StudySession, SolvedQuestion
from src.services.gemini import chat_gemini
from src.config import PROGRESSO_FILE
from src.services.file_store import save_model


def registrar_sessao_estudo(
    progresso: Progresso, materia: str, duracao_min: int, observacoes: str = ""
) -> Progresso:
    sessao = StudySession(
        materia=materia,
        duracao_min=duracao_min,
        observacoes=observacoes,
    )
    progresso.sessions.append(sessao)
    save_model(PROGRESSO_FILE, progresso)
    return progresso


def sugerir_plano_diario(
    config: StudyConfig,
    progresso: Progresso,
    questoes_resolvidas: list[SolvedQuestion],
    tags: dict[str, int] | None = None,
):

    # só mandamos um "resumo" para o modelo para não ficar gigante
    questoes_resumidas = [
        {"timestamp": str(q.timestamp), "enunciado": q.enunciado[:200]}
        for q in questoes_resolvidas
    ]

    prompt = f"""
Você é um coach de estudos para um estudante de {config.nivel},
que está se preparando para: {config.prova_alvo}.

CONFIGURAÇÃO DO ALUNO (planejamento):
{config.model_dump_json(ensure_ascii=False, indent=2)}

HISTÓRICO DE SESSÕES DE ESTUDO:
{progresso.model_dump_json(ensure_ascii=False, indent=2)}

HISTÓRICO RESUMIDO DE QUESTÕES RESOLVIDAS:
{json.dumps(questoes_resumidas, ensure_ascii=False, indent=2)}

Tarefa:
- Sugira um plano de estudo para HOJE em no máximo 12 linhas.
- Considere as matérias listadas em config.materias.
- Diga:
  - quais matérias/tópicos priorizar hoje
  - quantos blocos de estudo (ex: 3 blocos de 40–50 min)
  - quanto tempo reservar para:
      - revisão teórica
      - resolução de exercícios
      - revisão de questões erradas
  - se é melhor hoje revisar questões erradas ou aprender conteúdo novo
  - uma frase motivacional curta ao final, adequada a um aluno de {config.nivel}.
"""
    return chat_gemini(prompt)
