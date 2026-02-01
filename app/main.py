import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.parsers.detector import detect_and_parse
from typing import List

DEV = True

app = FastAPI()

@app.post("/parse")
async def parse_report(files: List[UploadFile] = File(...)):
    results = []
    errors = []
    
    for file in files:
        if not file.filename.lower().endswith(".csv"):
            errors.append({
                "filename": file.filename,
                "error": "Only CSV files supported"
            })
            continue

        contents = await file.read()
        text = contents.decode("utf-8", errors="ignore")

        try:
            result = detect_and_parse(text)
            results.append({
                "filename": file.filename,
                "data": result
            })
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "results": results,
        "errors": errors
    }
