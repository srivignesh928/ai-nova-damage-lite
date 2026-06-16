"""
=========================================================
Project : AI Powered Vehicle Valuation System
Module  : Damage Detection using AWS Bedrock Nova Lite
=========================================================
"""

import base64
import json
import io
from PIL import Image

from backend.app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    BEDROCK_MODEL_ID,
)
import boto3


def get_bedrock_client():
    """Initialize Bedrock Runtime client."""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def encode_image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def detect_vehicle_damage(image: Image.Image) -> dict:
    """
    Analyze vehicle damage using AWS Bedrock Nova Lite.
    Returns damage description and severity assessment.
    """
    client = get_bedrock_client()
    
    # Encode image
    image_base64 = encode_image_to_base64(image)
    
    # Structured prompt for damage detection
    prompt = """Analyze this image for vehicle damage. Look for scratches, dents, broken parts, tire damage, rust, paint issues, etc.

CRITICAL: You MUST respond with ONLY valid JSON. No other text before or after.

{
  "has_damage": true or false,
  "damage_description": "One sentence describing damage or 'No visible damage detected'",
  "severity": "none" or "minor" or "moderate" or "major",
  "detected_issues": ["issue1", "issue2"] or [],
  "confidence": 85
}

Rules:
- If this is NOT a vehicle image, return: has_damage=false, severity="none", damage_description="Not a vehicle image"
- If no damage visible, return: has_damage=false, severity="none", damage_description="No visible damage detected"
- Keep description under 150 characters
- confidence should be 0-100"""

    # Prepare request payload
    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "image": {
                            "format": "jpeg",
                            "source": {
                                "bytes": image_base64
                            }
                        }
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 300,
            "temperature": 0.2,
            "top_p": 0.9
        }
    }
    
    try:
        # Invoke Bedrock model
        response = client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json"
        )
        
        # Parse response
        response_body = json.loads(response["body"].read())
        
        # Debug: Print response structure
        print(f"Bedrock response keys: {response_body.keys()}")
        
        # Extract text from response
        output_text = response_body.get("output", {}).get("message", {}).get("content", [{}])[0].get("text", "")
        
        if not output_text:
            print(f"No text in response. Full response: {response_body}")
            raise ValueError("Empty response from Bedrock")
        
        print(f"Raw Bedrock output: {output_text[:200]}")
        
        # Clean JSON from markdown
        output_text = output_text.strip()
        if "```json" in output_text:
            output_text = output_text.split("```json")[1].split("```")[0].strip()
        elif "```" in output_text:
            output_text = output_text.split("```")[1].split("```")[0].strip()
        
        print(f"Cleaned output: {output_text[:200]}")
        
        result = json.loads(output_text)
        
        return {
            "has_damage": result.get("has_damage", False),
            "damage_description": result.get("damage_description", "Unable to analyze damage"),
            "severity": result.get("severity", "unknown"),
            "detected_issues": result.get("detected_issues", []),
            "confidence": result.get("confidence", 0),
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Failed to parse: {output_text if 'output_text' in locals() else 'N/A'}")
        return {
            "has_damage": False,
            "damage_description": "Unable to analyze damage right now. Please try a clearer image.",
            "severity": "unknown",
            "detected_issues": [],
            "confidence": 0,
        }
    except Exception as e:
        print(f"Damage detection error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return {
            "has_damage": False,
            "damage_description": f"Error analyzing damage: {str(e)}",
            "severity": "unknown",
            "detected_issues": [],
            "confidence": 0,
        }
