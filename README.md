## notes-to-quiz-generator-binod-kapadi-12201221
Quiz Generator automatically converts any set of notes or text into interactive quiz questions (MCQs or True/False) using AI.


## Project Overview
Convert your class notes or text into interactive quizzes using AI.


## Problem Statement
Students often take detailed notes but struggle to revise them effectively.
Manually creating quizzes from notes is time-consuming, making it hard to practice and retain knowledge efficiently.


## Solution Summary
I built Notes to Quiz Generator, an AI web app that converts notes or text into interactive quizzes automatically.
Users can paste notes or upload text files, and the backend uses FastAPI + Llama 3 / GPT API to generate MCQs, True/False, and short-answer questions with correct answers.


## Tech Stack
Backend: Python, FastAPI
Frontend: React.js / HTML + CSS
AI / LLM Models: OpenAI GPT-4 / Llama 3
Database: SQLite / MongoDB 
Deployment / Hosting: Vercel (frontend), Render (backend)
Version Control: Git + GitHub

## Project Structure



## Deployment



## Demo Video


## Features
- Converts text notes into interactive quizzes automatically.
- Generates multiple-choice, True/False, and short-answer questions.
- Clean, intuitive UI with real-time quiz generation.
- Real-world applicability for students, educators, and self-learners.


## Technical Architecture
The system takes user notes as input, sends them to an AI model for question generation, and displays the quiz results in the frontend.

Flow Steps:
   - User pastes notes → Frontend sends to backend
   - Backend processes input → Sends to AI model
   - AI model generates questions → Backend returns results
   - Frontend renders interactive quiz


## References


## License
This project is licensed under the MIT License.


## Acknowledgements


