import json

class CourseStructureAgent:
    def __init__(self, client, topic):
        self.client = client
        self.topic = topic

    def define_structure(self):
        system_prompt = (
            "Du bist ein Experte für Online-Kurserstellung mit Fokus auf Blended Learning und interaktive Lernformate. "
            "Antworte ausschließlich auf Deutsch und im JSON-Format. Die JSON-Struktur sollte so aussehen:"
            "{"
            "  'Module': ["
            "    {"
            "      'Name': 'string',"
            "      'Beschreibung': 'string',"
            "      'Lernziele': ['string'],"
            "      'Lektionen': ["
            "        {"
            "          'Name': 'string',"
            "          'Lernziele': ['string'],"
            "          'Beschreibung': 'string',"
            "          'Aktivitäten': ['string']"
            "        }"
            "      ],"
            "      'Projekt': {"
            "        'Beschreibung': 'string',"
            "        'Anforderungen': ['string']"
            "      }"
            "    }"
            "  ]"
            "}"
        )

        user_prompt = (
            f"Erstelle eine detaillierte und umfassende Kursstruktur auf Deutsch für das Thema '{self.topic}' basierend auf dem Blended Learning Ansatz. "
            f"Der Kurs sollte:"
            f"1. In logisch aufeinander aufbauende Module gegliedert sein."
            f"2. Jedes Modul sollte mehrere Lektionen enthalten, die verschiedene Aspekte des Themas abdecken."
            f"3. Für jedes Modul und jede Lektion klare Lernziele definieren."
            f"4. Eine Mischung aus theoretischen und praktischen Elementen beinhalten."
            f"5. Interaktive Aktivitäten und Übungen für jede Lektion vorschlagen."
            f"6. Ein abschließendes Projekt oder eine Fallstudie für jedes Modul enthalten."
            f"7. Genügend Tiefe und Breite bieten, um einen umfassenden Kurs zu erstellen."
            f"Stelle sicher, dass der Kurs engagierend, praxisorientiert und auf verschiedene Lernstile zugeschnitten ist."
        )

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
            response_format={"type": "json_object"}
        )

        structure = response.choices[0].message.content
        try:
            structure_json = json.loads(structure)
        except json.JSONDecodeError:
            print("Fehler beim Parsen des JSON.")
            structure_json = {"Module": []}
        
        return structure_json