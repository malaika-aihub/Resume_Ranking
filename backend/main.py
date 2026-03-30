# from fastapi import FastAPI, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import json, os, hashlib

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# USERS_FILE = "users.json"

# def load_users():
#     if not os.path.exists(USERS_FILE):
#         return {}
#     with open(USERS_FILE, "r") as f:
#         return json.load(f)

# def save_users(users):
#     with open(USERS_FILE, "w") as f:
#         json.dump(users, f)

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# @app.post("/login")
# def login(username: str = Form(...), password: str = Form(...)):
#     users = load_users()
#     hashed = hash_password(password)

#     if username not in users or users[username] != hashed:
#         raise HTTPException(status_code=401, detail="Invalid username or password")

#     token = hashlib.sha256(f"{username}:{hashed}".encode()).hexdigest()

#     return {"message": "Login successful", "token": token}

# @app.post("/signup")
# def signup(username: str = Form(...), password: str = Form(...)):
#     users = load_users()

#     if username in users:
#         raise HTTPException(status_code=400, detail="Username already exists")

#     users[username] = hash_password(password)
#     save_users(users)

#     return {"message": "Signup successful"}

# @app.post("/analyze")
# async def analyze(
#     api_key: str = Header(..., convert_underscores=True),
#     resumes: list[UploadFile] = File(...),
#     job_description: str = Form(...)
#     ):




# main.py
from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os, json, hashlib, jwt, datetime

# ---------- Config ----------
SECRET_KEY = os.getenv("SECRET_KEY")  # Use env var in production
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable not set!")

UPLOAD_DIR = "resumes"
USERS_FILE = "users.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- FastAPI setup ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # Replace with your frontend domain
    allow_methods=["*"],
    allow_headers=["*"]
)

security = HTTPBearer()

# ---------- Helpers ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def create_jwt(username: str):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=5)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ---------- Signup & Login ----------
@app.post("/signup")
def signup(username: str = Form(...), password: str = Form(...)):
    users = load_users()
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[username] = hash_password(password)
    save_users(users)
    return {"message": "Signup successful"}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    users = load_users()
    hashed = hash_password(password)
    if username not in users or users[username] != hashed:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_jwt(username)
    return {"message": "Login successful", "token": token}

# ---------- Analyze resumes ----------
@app.post("/analyze")
async def analyze(
    resumes: list[UploadFile] = File(...),
    job_description: str = Form(...),
    credentials: HTTPAuthorizationCredentials = security
):
    user = verify_jwt(credentials.credentials)

    # Save resumes to server
    uploaded_files = []
    for file in resumes:
        filename = os.path.basename(file.filename)
        path = os.path.join(UPLOAD_DIR, filename)
        with open(path, "wb") as f:
            f.write(await file.read())
        uploaded_files.append(path)

    # Dummy top_10 logic
    top_10 = [{
        "name": os.path.splitext(os.path.basename(f))[0],
        "match_score": 100,
        "skills": ["Python"],
        "experience": 2,
        "resume_path": f"/download_resume/{os.path.basename(f)}"
    } for f in uploaded_files[:10]]

    return {"top_10": top_10}

# ---------- Download resume ----------
@app.get("/download_resume/{filename}")
def download_resume(
    filename: str,
    credentials: HTTPAuthorizationCredentials = security
):
    user = verify_jwt(credentials.credentials)
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename
    )