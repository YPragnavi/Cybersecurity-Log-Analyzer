
from fastapi import FastAPI, UploadFile, File
from database import engine, SessionLocal
from models import Base, SecurityLog
import shutil
import os

app = FastAPI(title="Cybersecurity Log Analyzer")

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Cybersecurity Log Analyzer Running"}

@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "uploaded", "file": file.filename}

@app.get("/alerts")
def get_alerts():
    db = SessionLocal()
    return db.query(SecurityLog).all()
