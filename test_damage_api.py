#!/usr/bin/env python3
"""
Quick test for damage detection API endpoint
"""
import requests
from PIL import Image, ImageDraw
import io

# Create a test image with simulated damage
img = Image.new('RGB', (800, 600), color='lightgray')
draw = ImageDraw.Draw(img)

# Draw some "damage" patterns
draw.rectangle([100, 100, 400, 300], fill='darkgray', outline='red', width=5)
draw.ellipse([450, 150, 650, 350], fill='gray', outline='red', width=5)
draw.text((200, 400), "SCRATCHED", fill='red')

# Save to bytes
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

# Test the API
print("Testing /damage/analyze endpoint...")
print("-" * 50)

try:
    response = requests.post(
        'http://localhost:8000/damage/analyze',
        files={'damage_image': ('test_damage.jpg', img_bytes, 'image/jpeg')}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS!")
        print(f"Has Damage: {result['has_damage']}")
        print(f"Description: {result['damage_description']}")
        print(f"Severity: {result['severity']}")
        print(f"Issues: {result['detected_issues']}")
        print(f"Confidence: {result['confidence']}%")
    else:
        print(f"\n❌ FAILED: {response.text}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nMake sure the server is running:")
    print("python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload")
