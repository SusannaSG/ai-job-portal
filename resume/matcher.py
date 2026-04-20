import os
import re
import PyPDF2
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

STOP_WORDS = set(stopwords.words('english'))


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    else:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return ""


def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PDF error: {e}")
    return text


def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"DOCX error: {e}")
    return text


def preprocess_text(text):
    if not text or not text.strip():
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    filtered = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return " ".join(filtered)


def calculate_match_score(resume_text, job_text):
    clean_resume = preprocess_text(resume_text)
    clean_job    = preprocess_text(job_text)

    if not clean_resume or not clean_job:
        return 0.0

    try:
        vectorizer   = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_job])
        score = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]
        return round(float(score) * 100, 2)
    except Exception as e:
        print(f"Matching error: {e}")
        return 0.0


def get_ranked_jobs(resume_text, jobs_queryset):
    results = []
    for job in jobs_queryset:
        job_text = f"{job.description} {job.required_skills}"
        score    = calculate_match_score(resume_text, job_text)
        results.append({'job': job, 'score': score})
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


TECH_SKILLS = [
    'python', 'django', 'flask', 'javascript', 'react', 'nodejs',
    'java', 'spring', 'sql', 'mysql', 'postgresql', 'mongodb',
    'docker', 'kubernetes', 'aws', 'git', 'rest api', 'html', 'css',
    'machine learning', 'deep learning', 'pandas', 'numpy', 'tensorflow',
    'scikit-learn', 'nlp', 'power bi', 'excel', 'tableau',
]


def extract_skills_from_text(text):
    text_lower = text.lower()
    found = []
    for skill in TECH_SKILLS:
        if skill in text_lower:
            found.append(skill.title())
    return ', '.join(found)