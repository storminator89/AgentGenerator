import json
import os
import webbrowser
from agents.course_structure_agent import CourseStructureAgent
from agents.content_agent import ContentAgent
from agents.editing_agent import EditingAgent
from agents.qm_agent import QMAgent
from utils.config import get_groq_client
from json_to_html import generate_html_from_json, save_html_to_file

def save_course_progress(content, filename="online_kurs_zwischenergebnisse.json"):
    """Speichert den Kursinhalt als JSON-Datei."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"Zwischenergebnisse gespeichert: {filename}")

def create_online_course(topic, max_iterations=3):
    client = get_groq_client()

    print(f"Erstelle einen deutschsprachigen Online-Kurs zum Thema: {topic}")

    # Initialisiere die Agenten
    structure_agent = CourseStructureAgent(client, topic)
    content_agent = ContentAgent(client, topic)
    editing_agent = EditingAgent(client)
    qm_agent = QMAgent(client)

    # Schritt 1: Kursstruktur definieren
    print("Definiere Kursstruktur...")
    course_structure = structure_agent.define_structure()
    full_course_content = {}

    # Schritt 2: Inhalte generieren und bearbeiten
    for module in course_structure.get('Module', []):
        module_name = module.get('Name', 'Unbenanntes Modul')
        if module_name not in full_course_content:
            full_course_content[module_name] = {"Lektionen": {}, "Projekt": {}}
        
        for lesson in module.get('Lektionen', []):
            lesson_name = lesson.get('Name', 'Unbenannte Lektion')
            print(f"Generiere Inhalt für Modul '{module_name}', Lektion '{lesson_name}'...")
            content = content_agent.generate_content(module_name, lesson_name)
            
            # Bearbeite und verbessere den generierten Inhalt
            edited_content = editing_agent.edit_text(json.dumps(content))
            content = json.loads(edited_content)
            
            # Verbessere Übungen und Quizzes
            content['Übungen'] = json.loads(editing_agent.enhance_exercises(json.dumps(content.get('Übungen', []))))
            content['Quizzes'] = json.loads(editing_agent.improve_quizzes(json.dumps(content.get('Quizzes', []))))
            
            full_course_content[module_name]["Lektionen"][lesson_name] = content
        
        # Generiere Projektinhalt für das Modul
        print(f"Generiere Projektinhalt für Modul '{module_name}'...")
        project_content = content_agent.generate_content(module_name, "Projekt")
        edited_project_content = editing_agent.edit_text(json.dumps(project_content))
        full_course_content[module_name]["Projekt"] = json.loads(edited_project_content)

        # Speichere nach jeder Modulverarbeitung Zwischenergebnisse
        save_course_progress(full_course_content)

    # Schritt 3: Qualitätsprüfung und Verbesserung
    iteration = 0
    while iteration < max_iterations:
        overall_approved = True
        for module_name, module_content in full_course_content.items():
            print(f"Prüfe Qualität des Moduls '{module_name}'...")
            
            # Führe Qualitätsprüfung durch
            qm_feedback = qm_agent.quality_check(json.dumps({module_name: module_content}))
            print(f"QM-Feedback für Modul '{module_name}':", qm_feedback)

            # Führe technische Überprüfung durch
            tech_review = qm_agent.technical_review(json.dumps({module_name: module_content}), topic)
            print(f"Technische Überprüfung für Modul '{module_name}':", tech_review)

            if not qm_feedback.get("approved", False) or tech_review.get("technical_accuracy", 0) < 8:
                overall_approved = False
                
                # Verarbeite QM-Feedback
                for suggestion in qm_feedback.get("improvement_suggestions", []):
                    lesson = suggestion.get("lesson")
                    aspect = suggestion.get("aspect")
                    improvement = suggestion.get("suggestion")
                    print(f"Verbessere {aspect} in Lektion {lesson}: {improvement}")
                    
                    if lesson in module_content["Lektionen"]:
                        lesson_content = module_content["Lektionen"][lesson]
                        if aspect == "Inhalt":
                            improved_content = editing_agent.edit_text(json.dumps(lesson_content))
                            module_content["Lektionen"][lesson] = json.loads(improved_content)
                        elif aspect == "Übungen":
                            lesson_content['Übungen'] = json.loads(editing_agent.enhance_exercises(json.dumps(lesson_content.get('Übungen', []))))
                        elif aspect == "Quizzes":
                            lesson_content['Quizzes'] = json.loads(editing_agent.improve_quizzes(json.dumps(lesson_content.get('Quizzes', []))))
                
                # Verarbeite technisches Feedback
                for issue in tech_review.get("issues", []):
                    lesson = issue.get("lesson")
                    description = issue.get("description")
                    suggestion = issue.get("suggestion")
                    print(f"Technische Verbesserung in Lektion {lesson}: {description}")
                    
                    if lesson in module_content["Lektionen"]:
                        lesson_content = module_content["Lektionen"][lesson]
                        improved_content = editing_agent.edit_text(json.dumps(lesson_content))
                        module_content["Lektionen"][lesson] = json.loads(improved_content)

            # Speichere die Zwischenergebnisse nach jeder Überarbeitung
            save_course_progress(full_course_content)

        if overall_approved:
            print("Alle Module haben die Qualitätsprüfung bestanden.")
            break

        iteration += 1

    # Speichere den endgültigen Kurs
    save_course_progress(full_course_content, "online_kurs_final.json")
    print("Kurs erfolgreich erstellt und in 'online_kurs_final.json' gespeichert.")

    # Generiere HTML und öffne im Browser
    html_content = generate_html_from_json(full_course_content)
    html_filename = "moderner_online_kurs.html"
    save_html_to_file(html_content, html_filename)
    
    # Öffne die generierte HTML-Datei im Standard-Webbrowser
    webbrowser.open('file://' + os.path.realpath(html_filename))

if __name__ == "__main__":
    create_online_course("Wie funktioniert der SQL DELETE Befehl")