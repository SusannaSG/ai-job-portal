# 🤖 AI Job Portal with NLP Resume Matching

A Django-based job portal with AI-powered resume matching using NLP.

## Features
- 🔍 Browse and search job listings
- 📄 Upload resume (PDF/DOCX)
- 🤖 NLP-based resume matching using TF-IDF + Cosine Similarity
- 📊 Match score shown for each job (0-100%)
- 📋 Job application tracking with status updates
- 👤 User authentication (login/register)

## Tech Stack
- **Backend:** Django 6.0
- **NLP:** scikit-learn (TF-IDF + Cosine Similarity), NLTK
- **Database:** SQLite (development)
- **Frontend:** Bootstrap 5
- **PDF Parsing:** PyPDF2, python-docx

## How to Run
- git clone https://github.com/SusannaSG/ai-job-portal.git
- cd ai-job-portal
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver

## How NLP Matching Works
1. Resume text is extracted from PDF/DOCX
2. Text is cleaned using NLTK stopwords removal
3. TF-IDF vectorizer converts text to numbers
4. Cosine similarity compares resume vs job skills
5. Jobs are ranked by match score (highest first)