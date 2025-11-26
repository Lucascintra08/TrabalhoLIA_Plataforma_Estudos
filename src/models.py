# src/models.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class StudyConfig(BaseModel):
    # NOVO: nível de ensino
    nivel: str = Field(default="Ensino Médio")  # ou "Ensino Fundamental", etc.

    prova_alvo: str = Field(default="ENEM")
    horas_semana: int = Field(default=10, ge=1)
    materias: List[str] = Field(
        default_factory=lambda: ["Matemática", "Português", "Física"]
    )


class StudySession(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    materia: str
    duracao_min: int = Field(ge=1)
    observacoes: str = ""


class Progresso(BaseModel):
    sessions: List[StudySession] = Field(default_factory=list)


class SolvedQuestion(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    enunciado: str
    alternativas: Optional[str] = None
    resposta_aluno: Optional[str] = None
    materia: Optional[str] = None
    correcao_markdown: str


class AppState(BaseModel):
    config: StudyConfig
    progresso: Progresso
    questoes_resolvidas: List[SolvedQuestion] = Field(default_factory=list)
