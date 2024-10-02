import json
import re

def format_code_blocks(text):
    """Erkennt Codeblöcke in einem Text und formatiert sie mit <pre> und <code>."""
    if not isinstance(text, str):
        return str(text)
    
    # Spezielle Behandlung für SQL-Befehle
    if text.strip().upper().startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP')):
        return f'<pre><code class="language-sql">{text}</code></pre>'
    
    pattern = r'```(\w+)?\n(.*?)```'
    def replace(match):
        language = match.group(1) or 'sql'  # Standardmäßig SQL verwenden
        code = match.group(2)
        return f'<pre><code class="language-{language}">{code}</code></pre>'
    return re.sub(pattern, replace, text, flags=re.DOTALL)

def generate_html_from_json(data):
    html_content = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Moderner Online-Kurs</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-tomorrow.min.css" rel="stylesheet" />
        <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/plugins/line-numbers/prism-line-numbers.min.css" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-core.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/plugins/autoloader/prism-autoloader.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/plugins/line-numbers/prism-line-numbers.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-sql.min.js"></script>
        <style>
            body {
                font-family: 'Inter', sans-serif;
            }
            .sidebar {
                height: calc(100vh - 4rem);
                overflow-y: auto;
            }
            .content {
                height: calc(100vh - 4rem);
                overflow-y: auto;
            }
            .lesson-content {
                display: none;
            }
            .lesson-content.active {
                display: block;
            }
        </style>
    </head>
    <body class="bg-gray-100 text-gray-900">
        <nav class="bg-indigo-600 text-white p-4">
            <h1 class="text-2xl font-bold">Moderner Online-Kurs</h1>
        </nav>
        <div class="flex">
            <aside class="sidebar w-64 bg-white shadow-lg p-6">
                <h2 class="text-xl font-semibold mb-4">Inhaltsverzeichnis</h2>
                <ul class="space-y-2">
    """

    # Inhaltsverzeichnis erstellen
    for modul_name, module in data.items():
        html_content += f'<li><button class="module-btn text-left w-full font-semibold text-indigo-600 hover:text-indigo-800" data-module="{modul_name.replace(" ", "-")}">{modul_name}</button><ul class="pl-4 mt-2 space-y-1 hidden">'
        for lesson_name in module['Lektionen']:
            html_content += f'<li><button class="lesson-btn text-left w-full text-gray-700 hover:text-indigo-600" data-lesson="{lesson_name.replace(" ", "-")}">{lesson_name}</button></li>'
        html_content += '</ul></li>'
    
    html_content += """
                </ul>
            </aside>
            <main class="content flex-1 p-8">
    """

    # Module und Lektionen durchgehen
    for modul_name, module in data.items():
        html_content += f'<div id="{modul_name.replace(" ", "-")}" class="module">'
        for lesson_name, lesson in module['Lektionen'].items():
            html_content += f"""
            <div id="{lesson_name.replace(" ", "-")}" class="lesson-content">
                <h2 class="text-3xl font-bold mb-6">{lesson_name}</h2>
            """
            
            # Einführung
            if 'Einführung' in lesson:
                html_content += f'<div class="mb-6"><h3 class="text-2xl font-semibold mb-2">Einführung</h3><p>{lesson["Einführung"]}</p></div>'
            
            # Hauptinhalt
            if 'Hauptinhalt' in lesson:
                html_content += f'<div class="mb-6"><h3 class="text-2xl font-semibold mb-2">Hauptinhalt</h3><p>{lesson["Hauptinhalt"]}</p></div>'

            # Übungen anzeigen
            if 'Übungen' in lesson and lesson['Übungen']:
                html_content += '<div class="bg-white shadow-md rounded-lg p-6 mb-8"><h3 class="text-xl font-semibold mb-4">Übungen</h3>'
                exercises = lesson['Übungen'].get('exercises', [])
                for exercise in exercises:
                    title = exercise.get('title', 'Übung')
                    description = exercise.get('description', '')
                    solution = exercise.get('solution', '')
                    difficulty = exercise.get('difficulty', '')

                    formatted_solution = format_code_blocks(solution)
                    html_content += f"""
                    <div class="mb-4">
                        <h4 class="font-semibold">{title} <span class="text-sm text-gray-500">({difficulty})</span></h4>
                        <p class="mb-2">{description}</p>
                        <details>
                            <summary class="cursor-pointer text-indigo-600 hover:text-indigo-800">Lösung anzeigen</summary>
                            <div class="mt-2">{formatted_solution}</div>
                        </details>
                    </div>
                    """
                html_content += "</div>"

            # Quizzes anzeigen
            if 'Quizzes' in lesson and lesson['Quizzes']:
                html_content += '<div class="bg-white shadow-md rounded-lg p-6 mb-8"><h3 class="text-xl font-semibold mb-4">Quizzes</h3>'
                quizzes = lesson['Quizzes'].get('quizzes', [])
                for idx, quiz in enumerate(quizzes):
                    question = quiz.get('question', 'Keine Frage verfügbar')
                    choices = quiz.get('choices', [])
                    answer = quiz.get('correct_answer', '')
                    explanation = quiz.get('explanation', '')

                    html_content += f"""
                    <div class="quiz mb-6">
                        <p class="font-semibold mb-2">{question}</p>
                        <form class="space-y-2">
                    """
                    for choice_idx, choice in enumerate(choices):
                        html_content += f"""
                        <label class="flex items-center space-x-2">
                            <input type="radio" name="quiz_{idx}" class="form-radio text-indigo-600" value="{choice}">
                            <span>{choice}</span>
                        </label>
                        """
                    html_content += f"""
                        </form>
                        <button class="mt-2 bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 check-answer" data-answer="{answer}">Antwort überprüfen</button>
                        <p class="answer-feedback mt-2 hidden"></p>
                        <p class="explanation mt-2 hidden">{explanation}</p>
                    </div>
                    """
                html_content += "</div>"

            # Zusatzressourcen anzeigen
            if 'Zusatzressourcen' in lesson and lesson['Zusatzressourcen']:
                html_content += '<div class="bg-white shadow-md rounded-lg p-6 mb-8"><h3 class="text-xl font-semibold mb-4">Zusatzressourcen</h3><ul class="list-disc list-inside space-y-2">'
                for resource in lesson['Zusatzressourcen']:
                    html_content += f'<li><a href="{resource["link"]}" target="_blank" class="text-indigo-600 hover:text-indigo-800">{resource["type"]}: {resource["description"]}</a></li>'
                html_content += "</ul></div>"

            # Zusammenfassung
            if 'Zusammenfassung' in lesson:
                html_content += f'<div class="mb-6"><h3 class="text-2xl font-semibold mb-2">Zusammenfassung</h3><p>{lesson["Zusammenfassung"]}</p></div>'

            # Reflexion
            if 'Reflexion' in lesson:
                html_content += f'<div class="mb-6"><h3 class="text-2xl font-semibold mb-2">Reflexion</h3><p>{lesson["Reflexion"]}</p></div>'

            html_content += "</div>"
        html_content += "</div>"

    html_content += """
            </main>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', (event) => {
                function highlightCode() {
                    Prism.highlightAll();
                }

                // Aktiviere Zeilennummern für alle Code-Blöcke
                document.querySelectorAll('pre').forEach((block) => {
                    block.classList.add('line-numbers');
                });

                // Modul-Buttons
                document.querySelectorAll('.module-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const moduleId = btn.getAttribute('data-module');
                        const lessonList = btn.nextElementSibling;
                        lessonList.classList.toggle('hidden');
                    });
                });

                // Lektion-Buttons
                document.querySelectorAll('.lesson-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const lessonId = btn.getAttribute('data-lesson');
                        document.querySelectorAll('.lesson-content').forEach(content => {
                            content.classList.remove('active');
                        });
                        document.getElementById(lessonId).classList.add('active');
                        setTimeout(highlightCode, 0);
                    });
                });

                // Quiz-Überprüfung
                document.querySelectorAll('.check-answer').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const quiz = btn.closest('.quiz');
                        const selectedAnswer = quiz.querySelector('input[type="radio"]:checked');
                        const correctAnswer = btn.getAttribute('data-answer');
                        const feedback = quiz.querySelector('.answer-feedback');
                        const explanation = quiz.querySelector('.explanation');

                        if (selectedAnswer) {
                            if (selectedAnswer.value === correctAnswer) {
                                feedback.textContent = 'Richtig!';
                                feedback.classList.add('text-green-600');
                            } else {
                                feedback.textContent = 'Falsch. Versuche es noch einmal!';
                                feedback.classList.add('text-red-600');
                            }
                            feedback.classList.remove('hidden');
                            explanation.classList.remove('hidden');
                        } else {
                            alert('Bitte wähle eine Antwort aus.');
                        }
                    });
                });

                // Führe die Syntax-Hervorhebung durch, wenn eine Lösung angezeigt wird
                document.querySelectorAll('details').forEach(details => {
                    details.addEventListener('toggle', () => {
                        if (details.open) {
                            highlightCode();
                        }
                    });
                });

                // Zeige die erste Lektion standardmäßig an
                const firstLesson = document.querySelector('.lesson-content');
                if (firstLesson) {
                    firstLesson.classList.add('active');
                }

                // Führe die initiale Syntax-Hervorhebung durch
                highlightCode();
            });
        </script>
    </body>
    </html>
    """

    return html_content

def save_html_to_file(html_content, filename='moderner_online_kurs.html'):
    """Speichert die HTML-Datei auf dem Dateisystem."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML-Datei erfolgreich gespeichert: {filename}")

if __name__ == "__main__":
    # Lese die JSON-Datei ein
    with open('online_kurs_final.json', 'r', encoding='utf-8') as f:
        kurs_data = json.load(f)

    # Erstelle die HTML-Seite
    html_content = generate_html_from_json(kurs_data)

    # Speichere die HTML-Seite in eine Datei
    save_html_to_file(html_content)