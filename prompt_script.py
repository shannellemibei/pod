import os
from dotenv import load_dotenv
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import mimetypes
from analysis import analyze_image  

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
aiplatform.init(project=os.getenv("PROJECT_ID"))
model = GenerativeModel(os.getenv("MODEL_NAME"))  

def run_analysis(template_path: str, comparison_path: str, user_instructions: str, request_id: str, company_name: str):
    if not os.path.isfile(template_path) or not os.path.isfile(comparison_path):
        raise FileNotFoundError("One or both images not found.")

    template_bytes = open(template_path, "rb").read()
    mime_type, _ = mimetypes.guess_type(template_path)
    template_part = Part.from_data(data=template_bytes, mime_type=mime_type or "image/png")

    prefix = (
        "Analyze the structure and layout of the following template image. Mainly lets identify the logo of the company "
        "Generate a structured prompt that describes the expected format of any image that follows this template. "
        "Keep the prompt really short, we wanna know if the comparative  image is compliant or non compliant "
        "The prompt should specify that i strictly want one yes or no answer. If the image is compliant then give YES if not compliant say NO"
        "do not give me explanations_jusyt say yes or no"
        "These are proof of delivery documents so basicaly in the image we will scan based on the template, there should be a document in the image from company specified on tempelate, we are trying to prefent delivery scams hence proof od delivery documents"
    )
    if user_instructions:
        prefix += " Additional instructions: " + user_instructions

    generation_response = model.generate_content([prefix, template_part])
    generated_prompt = generation_response.text.strip()

    result = analyze_image(comparison_path, generated_prompt, request_id=request_id, company_name=company_name)

    return {
        "generated_prompt": generated_prompt,
        "result": result
    }

