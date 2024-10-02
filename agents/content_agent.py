from groq import Groq
import json

class ContentAgent:
    def __init__(self, client, topic):
        self.client = client
        self.topic = topic

    def generate_content(self, module, lesson):
        prompt = (
            f"Erstelle umfassenden und interaktiven Lerninhalt auf Deutsch für das Modul '{module}', Lektion '{lesson}' zum Thema '{self.topic}' im Blended Learning Format. "
            f"Der Inhalt sollte engagierend, praxisorientiert und auf verschiedene Lernstile zugeschnitten sein. "
            f"Inkludiere folgende Elemente:\n"
            f"1. Einführungstext mit klaren Lernzielen\n"
            f"2. Detaillierte Erklärungen mit Beispielen\n"
            f"3. Praktische Übungen mit steigendem Schwierigkeitsgrad\n"
            f"4. Interaktive Quizfragen zur Selbstüberprüfung\n"
            f"5. Vorschläge für ergänzende Ressourcen (Videos, Artikel, etc.)\n"
            f"6. Abschließende Zusammenfassung und Reflexionsaufgaben\n"
            f"Die Antwort muss im JSON-Format vorliegen und sollte folgende Struktur haben:\n"
            "{"
            "  'Einführung': 'string',"
            "  'Hauptinhalt': 'string',"
            "  'Übungen': [{'title': 'string', 'description': 'string', 'solution': 'string'}],"
            "  'Quizzes': [{'question': 'string', 'choices': ['string'], 'answer': 'string'}],"
            "  'Zusatzressourcen': [{'type': 'string', 'description': 'string', 'link': 'string'}],"
            "  'Zusammenfassung': 'string',"
            "  'Reflexion': 'string'"
            "}"
        )

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Du bist ein erfahrener Kursinhalt-Ersteller für deutschsprachige Bildungsinhalte mit Fokus auf interaktives und engagierendes Lernen. Antworte ausschließlich auf Deutsch und im JSON-Format."},
                {"role": "user", "content": prompt},
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
            response_format={"type": "json_object"}
        )

        content_text = response.choices[0].message.content
        try:
            content = json.loads(content_text)
        except json.JSONDecodeError:
            content = {
                "Einführung": "",
                "Hauptinhalt": content_text,
                "Übungen": [],
                "Quizzes": [],
                "Zusatzressourcen": [],
                "Zusammenfassung": "",
                "Reflexion": ""
            }
        return content