from sentence_transformers import SentenceTransformer, util
import torch
import os
from utils import clean_text

# Load BERT model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Important tech skills today
IMPORTANT_SKILLS = [
    "python", "ml", "machine learning", "deep learning", "nlp", 
    "data analysis", "sql", "azure", "aws", "cloud", "tensorflow", 
    "pytorch", "data science", "ai", "javascript", "react"
]

# Famous universities for small score boost
FAMOUS_UNIVERSITIES = [
    "MIT", "Stanford", "Harvard", "UC Berkeley", "Oxford", "Cambridge"
]

def extract_skills(text):
    text = text.lower()
    found = [skill for skill in IMPORTANT_SKILLS if skill.lower() in text]
    return found

def extract_education_score(text):
    text = text.lower()
    score = 0
    for uni in FAMOUS_UNIVERSITIES:
        if uni.lower() in text:
            score = 10  # max 10 points for education
            break
    return score

def extract_gpa_score(text):
    import re
    # Simple regex to find GPA like 3.5/4.0 or 4.0 scale
    gpa_match = re.search(r'(\d\.\d)[/\\]?4\.0', text)
    if gpa_match:
        gpa = float(gpa_match.group(1))
        return round((gpa / 4.0) * 10, 2)  # scale to 0-10
    return 0

def extract_experience_score(text):
    import re
    # Simple regex for "X years" experience
    match = re.search(r'(\d+)\s*years?', text.lower())
    if match:
        years = int(match.group(1))
        return min(years * 2, 30)  # max 30 points
    return 0

def rank_candidates_bert(resumes, job_description):
    jd_text = clean_text(job_description)
    resume_texts = [clean_text(r["text"]) for r in resumes]

    # BERT embeddings for skills context
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    resume_embeddings = model.encode(resume_texts, convert_to_tensor=True)

    similarities = util.cos_sim(jd_embedding, resume_embeddings)[0]

    candidates = []
    for i, sim in enumerate(similarities):
        resume_text = resume_texts[i]
        skills_found = extract_skills(resume_text)
        skills_score = round(len(skills_found) / len(IMPORTANT_SKILLS) * 50, 2)  # 50% weight
        experience_score = extract_experience_score(resume_text)                  # 30% weight
        education_score = extract_education_score(resume_text)                    # 10% weight
        gpa_score = extract_gpa_score(resume_text)                                # 10% weight

        # Combine total score
        total_score = skills_score + experience_score + education_score + gpa_score

        candidates.append({
            "name": os.path.basename(resumes[i]["filename"]),
            "match_score": round(total_score, 2),
            "skills": skills_found,
            "experience": experience_score // 2,  # approximate years
            "education_score": education_score,
            "gpa_score": gpa_score,
            "resume_url": f"uploads/{os.path.basename(resumes[i]['filename'])}"
        })

    # Sort top 10 by total score
    candidates.sort(key=lambda x: x["match_score"], reverse=True)
    return candidates[:10]
