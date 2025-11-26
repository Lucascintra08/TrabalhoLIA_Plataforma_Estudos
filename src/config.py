# src/config.py
from pathlib import Path
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Arquivos de dados locais
PROGRESSO_FILE = BASE_DIR / "progresso.json"
CONFIG_FILE = BASE_DIR / "config_estudos.json"
QUESTOES_FILE = BASE_DIR / "questoes_resolvidas.json"
