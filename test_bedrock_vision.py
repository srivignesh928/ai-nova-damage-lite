"""
Test AWS Bedrock Nova Lite Vision Integration
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.app.bedrock_vision import get_bedrock_client, analyze_vehicle_image_with_bedrock
from PIL import Image, ImageDraw, ImageFont

def test_bedrock_connection():
    """Test if Bedrock client can be initialized."""
    print("🔍 Testing Bedrock connection...")
    try:
        client = get_bedrock_client()
        print("✅ Bedrock client initialized successfully")
        print(f"   Region: {client.meta.region_name}")
        return True
    except Exception as e:
        print(f"❌ Bedrock connection failed: {e}")
        return False

def test_with_sample_image():
    """Test with a generated sample car image."""
    print("\n🖼️  Testing with sample image...")
    
    # Create a simple test image with text
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple car shape
    draw.rectangle([200, 250, 600, 450], fill='blue', outline='black', width=3)
    draw.rectangle([250, 200, 350, 250], fill='lightblue', outline='black', width=2)
    draw.rectangle([450, 200, 550, 250], fill='lightblue', outline='black', width=2)
    draw.ellipse([180, 420, 280, 480], fill='black')
    draw.ellipse([520, 420, 620, 480], fill='black')
    
    # Add text
    draw.text((300, 300), "MARUTI SWIFT", fill='white')
    
    print("   Created sample car image")
    
    try:
        result = analyze_vehicle_image_with_bedrock(img)
        print("✅ Bedrock analysis completed")
        print(f"   Detected Brand: {result.get('detected_brand')}")
        print(f"   Detected Model: {result.get('detected_model')}")
        print(f"   Body Type: {result.get('detected_body_type')}")
        print(f"   Color: {result.get('detected_color')}")
        print(f"   Confidence: {result.get('confidence')}%")
        return True
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("AWS Bedrock Nova Lite Vision Test")
    print("=" * 60)
    
    # Test 1: Connection
    connection_ok = test_bedrock_connection()
    
    if connection_ok:
        # Test 2: Image analysis
        test_with_sample_image()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
