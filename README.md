# POD Analysis API

This is an API for Proof of Delivery (POD) document analysis. It accepts a template image, a comparison image, and instructions, then uses a generative AI model to determine whether the comparison image aligns with the structure of the template.

## Functionality

- Accepts a template image and a comparison image via multipart/form-data.
- Generates a structured prompt based on the template and user instructions.
- Analyzes the comparison image against the generated prompt using a generative AI model.
- Logs request ID, company name, prompt, model response, and token usage.

## Request

POST /analyze/

Form fields:

- `template_image` (file): The reference/template image.
- `comparison_image` (file): The image to be checked.
- `user_instructions` (string): Optional text instructions to guide the prompt.
- `request_id` (string): Unique identifier for the request (used for logging).
- `company_name` (string): Name of the company related to the analysis (used in logs).

## Response

Example:

```json
{
  "request_id": "abc123",
  "generated_prompt": "Check if the document matches the expected layout with AcmeCorp logo...",
  "result": {
    "response": "Compliant. Document format matches the template layout.",
    "tokens": {
      "prompt": 87,
      "response": 65,
      "total": 152
    }
  }
}
```

## Logging

Logs are written to the `logs/` directory in files named by timestamp. Each log entry contains:

- Request ID and company name
- Image filename
- Prompt text
- Model response
- Token usage details

## Purpose

This system is designed to verify whether uploaded delivery documents follow a predefined structure, helping prevent fraud or format errors in POD workflows.
