# Online Course Creation Agent

## Project Overview

This program automates the creation of a fully developed online course in German. It utilizes various specialized agents to define course structure, generate content, edit and improve the material, and perform quality checks. At the end of the process, the course is saved as a JSON file and an HTML version is generated, which can be viewed in a web browser.

### Agents Used:

- **CourseStructureAgent**: Defines the structure of the course, including modules and lessons.
- **ContentAgent**: Generates the content for each lesson and project.
- **EditingAgent**: Edits and improves the generated content, exercises, and quizzes.
- **QMAgent**: Conducts quality and technical reviews to ensure the course meets the required standards.

## Functions

### `save_course_progress(content, filename="online_kurs_zwischenergebnisse.json")`
This function saves the current course progress into a JSON file.

### `create_online_course(topic, max_iterations=3)`
Main function that creates the course. The process consists of the following steps:

1. **Define Course Structure**: Using `CourseStructureAgent`, the structure of the course is created.
2. **Generate and Edit Content**: For each module and lesson, content is generated with `ContentAgent`, edited with `EditingAgent`, and enhanced with improved exercises and quizzes.
3. **Quality and Technical Review**: The course undergoes multiple iterations of review and improvement using `QMAgent` until all modules meet quality and technical accuracy standards.
4. **Save Final Course**: After all reviews, the course is saved as a final JSON file.
5. **Generate HTML**: An HTML version of the course is created and opened in the web browser.

## Usage

To create a new course, run the following command in your terminal:

```bash
python main.py