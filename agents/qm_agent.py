import json
from groq import Groq

class QMAgent:
    def __init__(self, client):
        self.client = client

    def quality_check(self, course_content):
        prompt = (
            "Führe eine umfassende Qualitätsprüfung des folgenden deutschsprachigen Kursinhalts durch. "
            "Bewerte die folgenden Aspekte:\n"
            "1. Klarheit und Verständlichkeit der Inhalte\n"
            "2. Vollständigkeit und Tiefe der Behandlung des Themas\n"
            "3. Didaktische Wertigkeit und Lernförderlichkeit\n"
            "4. Engagement und Interaktivität der Lernaktivitäten\n"
            "5. Angemessenheit der Übungen und Quizfragen\n"
            "6. Konsistenz und logischer Aufbau des Kurses\n"
            "7. Einhaltung der Lernziele\n"
            "8. Qualität der zusätzlichen Ressourcen\n"
            "9. Angemessenheit für die Zielgruppe\n"
            "10. Technische Korrektheit der Inhalte\n\n"
            "Gib detailliertes konstruktives Feedback und konkrete Verbesserungsvorschläge, "
            "um den Fokus auf den Lernenden zu stärken und die Gesamtqualität des Kurses zu erhöhen. "
            "Strukturiere dein Feedback im folgenden JSON-Format:\n"
            "{\n"
            '  "approved": boolean,\n'
            '  "overall_score": number, // 1-10\n'
            '  "feedback": {\n'
            '    "strengths": ["string"],\n'
            '    "weaknesses": ["string"]\n'
            '  },\n'
            '  "improvement_suggestions": [\n'
            '    {\n'
            '      "module": "Modulname",\n'
            '      "lesson": "Lektionenname",\n'
            '      "aspect": "string", // z.B. "Inhalt", "Übungen", "Quizzes"\n'
            '      "suggestion": "string"\n'
            '    }\n'
            '  ]\n'
            "}\n\n"
            f"Kursinhalt:\n{course_content}"
        )

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Du bist ein erfahrener Qualitätsmanager für deutschsprachige Online-Bildungsinhalte mit Fokus auf hohe Lernqualität und Lernerengagement. Antworte ausschließlich auf Deutsch und im JSON-Format."},
                {"role": "user", "content": prompt},
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
            response_format={"type": "json_object"}
        )

        qm_feedback_text = response.choices[0].message.content.strip()
        try:
            qm_feedback = json.loads(qm_feedback_text)
        except json.JSONDecodeError:
            qm_feedback = {
                "approved": False,
                "overall_score": 0,
                "feedback": {
                    "strengths": [],
                    "weaknesses": ["Fehler bei der Analyse des Kursinhalts"]
                },
                "improvement_suggestions": []
            }
        return qm_feedback

    def technical_review(self, course_content, topic):
        prompt = (
            f"Führe eine gründliche technische Überprüfung des deutschsprachigen Kursinhalts zum Thema '{topic}' durch. "
            "Konzentriere dich dabei auf:\n"
            "1. Technische Korrektheit aller Informationen und Codebeispiele\n"
            "2. Aktualität der Inhalte in Bezug auf den aktuellen Stand der Technik\n"
            "3. Vollständigkeit der technischen Erklärungen\n"
            "4. Angemessenheit der technischen Tiefe für das Zielpublikum\n"
            "5. Korrekte Verwendung von Fachbegriffen und Konzepten\n\n"
            "Gib dein Feedback im folgenden JSON-Format zurück:\n"
            "{\n"
            '  "technical_accuracy": number, // 1-10\n'
            '  "issues": [\n'
            '    {\n'
            '      "module": "string",\n'
            '      "lesson": "string",\n'
            '      "description": "string",\n'
            '      "suggestion": "string"\n'
            '    }\n'
            '  ],\n'
            '  "recommendations": ["string"]\n'
            "}\n\n"
            f"Kursinhalt:\n{course_content}"
        )

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"Du bist ein technischer Experte im Bereich {topic} mit umfangreicher Erfahrung in der Überprüfung von deutschsprachigen Bildungsinhalten. Antworte ausschließlich auf Deutsch und im JSON-Format."},
                {"role": "user", "content": prompt},
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
            response_format={"type": "json_object"}
        )

        tech_review_text = response.choices[0].message.content.strip()
        try:
            tech_review = json.loads(tech_review_text)
        except json.JSONDecodeError:
            tech_review = {
                "technical_accuracy": 0,
                "issues": [],
                "recommendations": ["Fehler bei der technischen Überprüfung des Kursinhalts"]
            }
        return tech_review