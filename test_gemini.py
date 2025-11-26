from google import genai

# COLE SUA CHAVE DIRETO AQUI TEMPORARIAMENTE
API_KEY = "AIzaSyDYALodeKFDG8vFOUZkmcsUD2ZckT8kSFo"

client = genai.Client(api_key=API_KEY)

resp = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explique rapidamente o que é dor neuropática em 3 linhas."
)

print(resp.text)