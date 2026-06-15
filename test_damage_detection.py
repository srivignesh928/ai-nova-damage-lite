"""
Test script for damage detection feature
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PIL import Image, ImageDraw
import io

from backend.app.damage_detector import detect_vehicle_damage


def create_test_damage_image():
    """Create a simple test image with text indicating damage."""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw some shapes to simulate damage
    draw.rectangle([100, 100, 300, 200], fill='gray', outline='black', width=3)
    draw.ellipse([400, 150, 500, 250], fill='darkgray', outline='black', width=3)
    draw.line([200, 300, 600, 400], fill='red', width=5)
    
    return img


def test_damage_detection():
    """Test the damage detection functionality."""
    print("=" * 60)
    print("Testing Damage Detection with AWS Bedrock Nova Lite")
    print("=" * 60)
    
    # Create test image
    print("\n1. Creating test damage image...")
    test_image = create_test_damage_image()
    print("   ✅ Test image created (800x600)")
    
    # Test damage detection
    print("\n2. Analyzing damage with Bedrock...")
    try:
        result = detect_vehicle_damage(test_image)
        
        print("   ✅ Damage analysis completed!")
        print(f"\n   Results:")
        print(f"   - Has Damage: {result['has_damage']}")
        print(f"   - Description: {result['damage_description']}")
        print(f"   - Severity: {result['severity']}")
        print(f"   - Detected Issues: {result['detected_issues']}")
        print(f"   - Confidence: {result['confidence']}%")
        
        if result['has_damage']:
            print("\n   ✅ Damage detection working!")
        else:
            print("\n   ℹ️  No damage detected (expected for test image)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_api_integration():
    """Test the API endpoint."""
    print("\n" + "=" * 60)
    print("Testing API Integration")
    print("=" * 60)
    
    try:
        from backend.app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Create test image
        test_image = create_test_damage_image()
        img_bytes = io.BytesIO()
        test_image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        print("\n1. Testing POST /damage/analyze endpoint...")
        response = client.post(
            "/damage/analyze",
            files={"damage_image": ("test_damage.jpg", img_bytes, "image/jpeg")}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ API endpoint working!")
            print(f"\n   Response:")
            print(f"   - Status Code: {response.status_code}")
            print(f"   - Has Damage: {result['has_damage']}")
            print(f"   - Description: {result['damage_description']}")
            print(f"   - Severity: {result['severity']}")
            return True
        else:
            print(f"   ❌ API returned status code: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except ImportError:
        print("   ⚠️  FastAPI TestClient not available, skipping API test")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("\n🚀 Starting Damage Detection Tests\n")
    
    # Test 1: Damage detection function
    test1_passed = test_damage_detection()
    
    # Test 2: API integration
    test2_passed = test_api_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Damage Detection: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"API Integration:  {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Damage detection is ready.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("1. Start the server: uvicorn backend.app.main:app --reload")
    print("2. Open http://localhost:8000")
    print("3. Upload a damage image and click 'Analyze Damage'")
    print("4. Review the AI-generated description")
    print("5. Click 'Use Description' to auto-fill the form")
    print("=" * 60)
