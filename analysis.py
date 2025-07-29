import os
from dotenv import load_dotenv
from google.cloud import aiplatform 
from vertexai.generative_models import GenerativeModel, Part
import mimetypes
from datetime import datetime


log_file = f"logs/run_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
os.makedirs("logs", exist_ok=True)

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
aiplatform.init(project=os.getenv("PROJECT_ID"))
model = GenerativeModel(os.getenv("MODEL_NAME"))

def read_image(path):
    with open(path, "rb") as f:
        return f.read()

def analyze_image(image_path: str, prompt_text: str, request_id: str, company_name: str) -> dict:
    if not os.path.isfile(image_path):
        raise FileNotFoundError("Image not found.")

    image_bytes = read_image(image_path)
    mime_type, _ = mimetypes.guess_type(image_path)
    image_part = Part.from_data(data=image_bytes, mime_type=mime_type or "image/png")

    response = model.generate_content([prompt_text, image_part])

    prompt_tokens = response.usage_metadata.prompt_token_count if response.usage_metadata else "N/A"
    response_tokens = response.usage_metadata.candidates_token_count if response.usage_metadata else "N/A"
    total_tokens = response.usage_metadata.total_token_count if response.usage_metadata else "N/A"

    response_text = response.text.strip()

    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"\n--- Request ID: {request_id} | Company: {company_name} ---\n")
        log.write(f"Image: {os.path.basename(image_path)}\n")
        log.write(f"Prompt:\n{prompt_text}\n")
        log.write(f"Response:\n{response_text}\n")
        log.write(f"Tokens Used - Prompt: {prompt_tokens}, Response: {response_tokens}, Total: {total_tokens}\n")

    return {
        "response": response_text,
        "tokens": {
            "prompt": prompt_tokens,
            "response": response_tokens,
            "total": total_tokens
        }
    }
