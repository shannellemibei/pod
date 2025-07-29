from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import shutil
import uuid

from prompt_script import run_analysis  

app = FastAPI()

@app.post("/analyze/")
async def analyze(
    template_image: UploadFile = File(...),
    comparison_image: UploadFile = File(...),
    user_instructions: str = Form(...),
    request_id: str = Form(...),           
    company_name: str = Form(...)          
):
    os.makedirs("temp", exist_ok=True)

    def save_temp_file(upload: UploadFile):
        ext = os.path.splitext(upload.filename)[1]
        tmp_name = f"{uuid.uuid4()}{ext}"
        path = os.path.join("temp", tmp_name)
        with open(path, "wb") as f:
            shutil.copyfileobj(upload.file, f)
        return path

    template_path = save_temp_file(template_image)
    comparison_path = save_temp_file(comparison_image)

    try:
        result = run_analysis(
            template_path, comparison_path, user_instructions,
            request_id=request_id, company_name=company_name
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "request_id": request_id})
    finally:
        os.remove(template_path)
        os.remove(comparison_path)

    return {"request_id": request_id, **result}

