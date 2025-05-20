# Memoria: Intelligent Flashcard Generation System

Memoria is an AI-powered platform that automatically generates and manages flashcards to help users learn vocabulary efficiently. By leveraging advanced NLP and speech technologies, Memoria transforms various document types into interactive learning material for personalized study experiences.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [System Requirements](#system-requirements)
5. [Installation](#installation)
    - [Front-end Setup](#front-end-setup)
    - [Back-end Setup](#back-end-setup)
    - [Database Setup](#database-setup)
    - [API Key Setup](#api-key-setup)
6. [Usage Workflow](#usage-workflow)
7. [Documentation](#documentation)
8. [License](#license)

## Overview

Memoria enables users to generate flashcards from diverse content (structured and unstructured text, including DOCX, PPTX, and PDF) and provides an interactive platform for vocabulary learning. Users can review, edit, and practice flashcards, check pronunciation, and interact with an in-app QnA chatbot trained on their documents.

## Features

- **Automatic Flashcard Generation**  
  Upload documents and automatically extract vocabulary and descriptions using AI (ChatGPT API).
- **Flexible Input Handling**  
  Supports both structured and unstructured text files (including DOCX, PPTX, PDF).
- **Personalized Topics & Histories**  
  Organizes flashcards by topics; tracks both learned and unlearned words per user.
- **Interactive Learning**  
  Swipe/flip flashcard UI for marking learning status; review vocabulary and descriptions.
- **Flashcard Editing**  
  Edit flashcards before saving to your set for true personalization.
- **Pronunciation Assistance**  
  See IPA, listen to native pronunciation, and use speech scoring to practice your own pronunciation.
- **QnA Chatbot**  
  Ask questions about your own uploaded vocabulary; chatbot answers based on user-uploaded documents only.
- **Security**  
  Document filtering to avoid malicious or inappropriate content.

## Technologies Used

### Front-end
- **React** (with Next.js)
- **TailwindCSS** for styling
- **Hero UI** component library

### Back-end
- **Python** (Django framework)
- **Django REST Framework**
- **Integration with OpenAI, Gemini, Elevenlabs API**

### Database
- **PostgreSQL** (configured via Django settings)

## System Requirements

- **Python 3.11+**
- **pipenv**
- **Node.js (v16+) & npm/yarn**
- **PostgreSQL**

## Installation

### <a name="front-end-setup"></a>Front-end Setup

```bash
cd client/memoria
npm install
npm run dev
```
> The front-end is built with Next.js (React). It uses TailwindCSS and Hero UI for styling and UI components.

### <a name="back-end-setup"></a>Back-end Setup

```bash
cd server
pipenv shell
pipenv sync
python manage.py migrate
python manage.py runserver
```
> The back-end uses Django and Django REST Framework. Make sure your database is set up before running migrations.

### <a name="database-setup"></a>Database Setup

- Ensure PostgreSQL is installed and running.
- Create a new database (e.g., `memoria`), user, and password.
- Update your database settings in `server/settings.py`:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'memoria',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
- Install PostgreSQL drivers for Python if prompted (`pipenv install psycopg2`).

### <a name="api-key-setup"></a>API Key Setup

- Create an environment file (`.env`) in [`server/memoria/`](./server/memoria/)
- Set up your OpenAI, Gemini, Elevenlabs API keys in that file:
  ```bash
  OPENAI_API_KEY=<your_api_key>
  ELEVENLABS_API_KEY=<your_api_key>
  GEMINI_API_KEY=<your_api_key>
  ```

## Usage Workflow

1. **Upload Document:**  
   User uploads a DOCX, PPTX, PDF, or text document and sets the desired number of flashcards.
2. **Flashcard Extraction:**  
   Front-end sends the file to the back-end, which calls the ChatGPT API for vocabulary extraction and risk filtering.
3. **Review & Edit:**  
   Extracted flashcards are displayed. User can edit cards before saving.
4. **Save to Topic:**  
   Finalized flashcards are saved as a topic in the user’s collection.
5. **Learning Session:**  
   Users select a topic and learn using swipe/flip UI, check IPA/pronunciation, and interact with the QnA chatbot.
6. **Progress Tracking:**  
   System maintains history of learned/unlearned words for each topic.

## Documentation

- For detailed information of the project, see [`Report.pdf`](.docs/Report.pdf).

## License

Distributed under the terms of the [LICENSE](./LICENSE) file in this repository.

> For questions, feature requests, or contributions, please open an issue or pull request!