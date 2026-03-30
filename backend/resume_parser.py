import pdfplumber

def parse_resumes(file_paths):
    resumes = []
    for path in file_paths:
        with pdfplumber.open(path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        resumes.append({"filename": path, "text": text})
    return resumes
