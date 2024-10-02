import json
from groq import Groq

class EditingAgent:
    def __init__(self, client):
        self.client = client

    def edit_text(self, content):
        prompt = (
            "Überarbeite und optimiere den folgenden Kursinhalt auf Deutsch, um Klarheit, Präzision und Lesbarkeit zu verbessern. "
            "Achte dabei auf folgende Aspekte:\n"
            "1. Verbessere die Struktur und den Lesefluss.\n"
            "2. Stelle sicher, dass der Inhalt didaktisch wertvoll und für Lernende ansprechend formuliert ist.\n"
            "3. Füge bei Bedarf erklärende Beispiele oder Analogien hinzu.\n"
            "4. Optimiere die Sprache für besseres Verständnis und Engagement.\n"
            "5. Stelle sicher, dass die Lernziele klar kommuniziert werden.\n"
            "6. Verbessere die Übergänge zwischen verschiedenen Abschnitten.\n"
            "7. Füge, wo angemessen, Hervorhebungen oder Aufzählungen hinzu.\n\n"
            "Behalte die ursprüngliche JSON-Struktur bei und gib den überarbeiteten Inhalt im gleichen JSON-Format zurück.\n\n"
            f"Inhalt:\n{content}"
        )

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Du bist ein professioneller Lektor und Pädagoge mit Spezialisierung auf deutschsprachige Bildungsinhalte und E-Learning. Antworte ausschließlich auf Deutsch und im JSON-Format."},
                {"role": "user", "content": prompt},
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
            response_format={"type": "json_object"}
        )
        
        edited_content = response.choices[0].message.content.strip()
        return edited_content

    def enhance_exercises(self, exercises):
        prompt = (
            "Verbessere und erweitere die folgenden Übungen auf Deutsch, um sie interaktiver und lernfördernder zu gestalten. "
            "Achte dabei auf:\n"
            "1. Klarheit der Anweisungen\n"
            "2. Steigerung des Schwierigkeitsgrads\n"
            "3. Praxisbezug und Relevanz\n"
            "4. Förderung kritischen Denkens\n"
            "5. Möglichkeiten zur Selbstreflexion\n\n"
            "Gib deine Antwort als JSON-Objekt zurück, das ein Array von Übungen unter dem Schlüssel 'exercises' enthält. Jede Übung sollte folgende Struktur haben:\n"
            "{\n"
            '  "exercises": [\n'
            '    {\n'
            '      "title": "string",\n'
            '      "description": "string",\n'
            '      "solution": "string",\n'
            '      "difficulty": "string" // z.B. "Einfach", "Mittel", "Schwer"\n'
            '    }\n'
            '  ]\n'
            "}\n\n"
            f"Übungen:\n{exercises}"
        )

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Du bist ein erfahrener Pädagoge mit Expertise in der Erstellung effektiver Lernübungen. Antworte ausschließlich auf Deutsch und im JSON-Format."},
                {"role": "user", "content": prompt},
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
            response_format={"type": "json_object"}
        )
        
        enhanced_exercises_text = response.choices[0].message.content.strip()
        try:
            enhanced_exercises = json.loads(enhanced_exercises_text)
            if not isinstance(enhanced_exercises.get('exercises', []), list):
                enhanced_exercises['exercises'] = [enhanced_exercises.get('exercises', {})]
        except json.JSONDecodeError:
            enhanced_exercises = {"exercises": []}
        
        return json.dumps(enhanced_exercises)

    def improve_quizzes(self, quizzes):
        prompt = (
            "Optimiere die folgenden Quizfragen auf Deutsch, um das Lernen und die Selbstüberprüfung zu verbessern. "
            "Achte dabei auf:\n"
            "1. Klarheit und Präzision der Fragen\n"
            "2. Relevanz für die Lernziele\n"
            "3. Variation der Fragetypen (Multiple Choice, Wahr/Falsch, Lückentexte etc.)\n"
            "4. Angemessenen Schwierigkeitsgrad\n"
            "5. Informatives Feedback zu richtigen und falschen Antworten\n\n"
            "Gib deine Antwort als JSON-Objekt zurück, das ein Array von Quizfragen unter dem Schlüssel 'quizzes' enthält. Jede Frage sollte folgende Struktur haben:\n"
            "{\n"
            '  "quizzes": [\n'
            '    {\n'
            '      "question": "string",\n'
            '      "type": "string", // z.B. "multiple_choice", "true_false", "fill_in_blank"\n'
            '      "choices": ["string"], // Nur für Multiple Choice\n'
            '      "correct_answer": "string",\n'
            '      "explanation": "string" // Erklärung zur richtigen Antwort\n'
            '    }\n'
            '  ]\n'
            "}\n\n"
            f"Quizfragen:\n{quizzes}"
        )

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Du bist ein Experte für die Erstellung effektiver Lernüberprüfungen und Quizfragen. Antworte ausschließlich auf Deutsch und im JSON-Format."},
                {"role": "user", "content": prompt},
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
            response_format={"type": "json_object"}
        )
        
        improved_quizzes_text = response.choices[0].message.content.strip()
        try:
            improved_quizzes = json.loads(improved_quizzes_text)
            if not isinstance(improved_quizzes.get('quizzes', []), list):
                improved_quizzes['quizzes'] = [improved_quizzes.get('quizzes', {})]
        except json.JSONDecodeError:
            improved_quizzes = {"quizzes": []}
        
        return json.dumps(improved_quizzes)