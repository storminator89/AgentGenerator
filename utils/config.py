import os
from dotenv import load_dotenv
from groq import Groq

# Lade Umgebungsvariablen aus der .env Datei
load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)