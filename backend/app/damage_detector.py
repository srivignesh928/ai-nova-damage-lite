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
    prompt = """Analyze this vehicle image for any damage, defects, or issues. 
Identify specific problems like scratches, dents, broken parts, tire damage, rust, paint issues, etc.

Return ONLY valid JSON in this exact format:
{
  "has_damage": true/false,
  "damage_description": "One clear sentence describing all visible damage",
  "severity": "minor/moderate/major/none",
  "detected_issues": ["issue1", "issue2"],
  "confidence": 0-100
}

Important: 
- Be specific about location and type of damage
- If no damage visible, set has_damage to false and damage_description to "No visible damage detected"
- Keep description concise but informative (max 150 characters)
- Focus on actual damage, not normal wear"""

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
        output_text = response_body.get("output", {}).get("message", {}).get("content", [{}])[0].get("text", "{}")
        
        # Clean JSON from markdown
        output_text = output_text.strip()
        if "```json" in output_text:
            output_text = output_text.split("```json")[1].split("```")[0].strip()
        elif "```" in output_text:
            output_text = output_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(output_text)
        
        return {
            "has_damage": result.get("has_damage", False),
            "damage_description": result.get("damage_description", "Unable to analyze damage"),
            "severity": result.get("severity", "unknown"),
            "detected_issues": result.get("detected_issues", []),
            "confidence": result.get("confidence", 0),
        }
        
    except Exception as e:
        print(f"Damage detection error: {e}")
        return {
            "has_damage": False,
            "damage_description": "Error analyzing damage image",
            "severity": "unknown",
            "detected_issues": [],
            "confidence": 0,
        }
