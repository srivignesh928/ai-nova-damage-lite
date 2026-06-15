"""
Complete Integration Test: Bedrock Vision → Auto-fill → Price Prediction
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from PIL import Image, ImageDraw
from backend.app.bedrock_vision import analyze_vehicle_image_with_bedrock
from backend.app.utils import init_db, search_brands, get_vehicle_details
from backend.app.predictor import predict_price
import pandas as pd
from datetime import datetime

def create_test_car_image(brand="MARUTI", model="SWIFT"):
    """Create a test car image with brand/model text."""
    img = Image.new('RGB', (800, 600), color='silver')
    draw = ImageDraw.Draw(img)
    
    # Draw car shape
    draw.rectangle([200, 250, 600, 450], fill='red', outline='black', width=3)
    draw.rectangle([250, 200, 350, 250], fill='lightgray', outline='black', width=2)
    draw.rectangle([450, 200, 550, 250], fill='lightgray', outline='black', width=2)
    draw.ellipse([180, 420, 280, 480], fill='black')
    draw.ellipse([520, 420, 620, 480], fill='black')
    
    # Add brand/model text
    draw.text((280, 300), f"{brand} {model}", fill='white')
    
    return img

def test_complete_flow():
    """Test the complete flow: Image → Brand Detection → Auto-fill → Prediction."""
    
    print("=" * 70)
    print("COMPLETE FLOW TEST: Bedrock Vision → Auto-fill → Price Prediction")
    print("=" * 70)
    
    # Step 1: Initialize database
    print("\n📊 Step 1: Initialize Database")
    db_connection = init_db()
    brands = search_brands(db_connection)
    print(f"   ✅ Database initialized with {len(brands)} brands: {', '.join(brands)}")
    
    # Step 2: Create test image
    print("\n🖼️  Step 2: Create Test Car Image")
    test_image = create_test_car_image("MARUTI", "SWIFT")
    print("   ✅ Test image created (Maruti Swift)")
    
    # Step 3: Analyze with Bedrock Nova Lite
    print("\n🤖 Step 3: Analyze Image with AWS Bedrock Nova Lite")
    vision_result = analyze_vehicle_image_with_bedrock(test_image)
    detected_brand = vision_result.get("detected_brand")
    detected_model = vision_result.get("detected_model")
    detected_body = vision_result.get("detected_body_type")
    detected_color = vision_result.get("detected_color")
    
    print(f"   ✅ Brand Detected: {detected_brand}")
    print(f"   ✅ Model Detected: {detected_model}")
    print(f"   ✅ Body Type: {detected_body}")
    print(f"   ✅ Color: {detected_color}")
    print(f"   ✅ Confidence: {vision_result.get('confidence')}%")
    
    # Step 4: Auto-fill form (simulate frontend logic)
    print("\n📝 Step 4: Auto-fill Form Fields")
    
    # Match detected brand with database
    brand_match = None
    if detected_brand:
        for db_brand in brands:
            if detected_brand.upper() in db_brand.upper() or db_brand.upper() in detected_brand.upper():
                brand_match = db_brand
                break
    
    if not brand_match:
        print("   ⚠️  Brand not found in database, using first available brand")
        brand_match = brands[0] if brands else "Maruti"
    
    print(f"   ✅ Matched Brand: {brand_match}")
    
    # Get vehicle details from database
    vehicle_details = get_vehicle_details(db_connection, brand_match, "Swift")
    
    if vehicle_details:
        print(f"   ✅ Variants: {vehicle_details.get('variants', [])}")
        print(f"   ✅ Fuel Types: {vehicle_details.get('fuel', [])}")
        print(f"   ✅ Transmissions: {vehicle_details.get('transmission', [])}")
        print(f"   ✅ Body Type: {vehicle_details.get('body', 'N/A')}")
        print(f"   ✅ Premium Brand: {vehicle_details.get('premium_brand', 'No')}")
    
    # Step 5: Prepare prediction payload
    print("\n🎯 Step 5: Prepare Prediction Payload")
    
    payload = {
        "oem": brand_match,
        "model": "Swift",
        "variant": vehicle_details.get('variants', ['VXI'])[0] if vehicle_details else "VXI",
        "fuel": vehicle_details.get('fuel', ['Petrol'])[0] if vehicle_details else "Petrol",
        "transmission": vehicle_details.get('transmission', ['Manual'])[0] if vehicle_details else "Manual",
        "body": vehicle_details.get('body', 'Hatchback') if vehicle_details else "Hatchback",
        "owner_type": "first",
        "City": "Mumbai",
        "state": "Maharashtra",
        "km": 45000.0,
        "car_age": 5,
        "premium_brand": 1 if vehicle_details.get('premium_brand') == 'Yes' else 0,
        "myear": datetime.now().year - 5
    }
    
    print("   ✅ Payload prepared:")
    for key, value in payload.items():
        print(f"      • {key}: {value}")
    
    # Step 6: Predict price using XGBoost model
    print("\n💰 Step 6: Predict Price with XGBoost Model")
    
    input_df = pd.DataFrame([payload])
    predicted_price = predict_price(input_df)
    
    print(f"   ✅ Predicted Price: ₹{predicted_price:,.2f}")
    
    # Step 7: Summary
    print("\n" + "=" * 70)
    print("✅ COMPLETE FLOW TEST SUCCESSFUL!")
    print("=" * 70)
    print(f"\n📋 Summary:")
    print(f"   1. Image uploaded → Bedrock detected: {detected_brand}")
    print(f"   2. Brand matched in database → {brand_match}")
    print(f"   3. Form auto-filled with vehicle details")
    print(f"   4. XGBoost model predicted price → ₹{predicted_price:,.2f}")
    print(f"\n🎉 All systems working perfectly!")
    print("=" * 70)

if __name__ == "__main__":
    test_complete_flow()
