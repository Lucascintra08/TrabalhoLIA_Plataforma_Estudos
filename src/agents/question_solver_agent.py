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
Você é um professor especialista em {materia or "disciplinas do ensino médio"}
e seu objetivo é ENSINAR e não apenas dar a resposta.

Você deve corrigir a seguinte questão:

📘 **Enunciado da questão:**
\"\"\"{enunciado}\"\"\"


📑 **Alternativas (se houver):**
\"\"\"{alternativas or "Questão dissertativa — não há alternativas."}\"\"\"

📌 **Resposta marcada pelo aluno (se houver):** {resposta_aluno or "não informada"}
📚 **Matéria/Tema:** {materia or "não informado"}
🎓 **Nível do aluno:** {nivel or "ensino médio"}

---

## 🧠 Tarefas:

**1. Gabarito**
- Diga qual é a resposta correta (letra ou texto).
- Seja direto, sem justificativas aqui.

**2. Raciocínio guiado**
Explique o passo a passo como para um aluno:
- Defina os conceitos envolvidos.
- Mostre o caminho lógico da solução.
- Evite saltos matemáticos impossíveis.
- Não use linguagem excessivamente técnica.

**3. Análise pedagógica das alternativas**
Para cada alternativa:
- Explique *por que está errada*.
- Aponte *error comum de aluno* ao escolher aquela alternativa.
- Exemplos:
  - erro de sinal
  - confusão de fórmulas
  - interpretação errada

**4. Macete / Dica de memorização**
- 1–2 frases curtas
- objetivo: lembrar no momento da prova

**5. Assunto / TAG**
- 1 tag curta (1–3 palavras)
- exemplos: “Funções”, “Óptica”, “Citologia”, “Derivadas”
- sem frases longas, sem hashtags

---

## 📦 FORMATO FINAL (obrigatório)

### **Gabarito**
⚠️ Resposta correta: **...**

### **Raciocínio comentado**
Texto passo a passo

### **Análise das alternativas**
- A) ...
- B) ...
- C) ...
- D) ...

### **Dica de memorização**
...

### **Assunto / Tag**
...

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
