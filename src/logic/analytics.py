from collections import Counter
from src.models import SolvedQuestion

def contar_tags(questoes: list[SolvedQuestion]):
    tags = [q.materia for q in questoes if q.materia]
    return dict(Counter(tags))
