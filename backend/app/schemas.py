from pydantic import BaseModel


class VehicleInput(BaseModel):
    oem: str
    model: str
    variant: str
    fuel: str
    transmission: str
    body: str
    owner_type: str
    City: str
    state: str
    km: int
    car_age: int
    premium_brand: int
    damage_description: str | None = None
    transaction_type: str = "selling"


class PredictionResponse(BaseModel):
    predicted_price: float
    damage_cost: float
    confidence_score: float
    suggested_price: float
    currency: str
    model_version: str
    status: str
    transaction_type: str
    transaction_price: float
    profit_margin: float | None
    price_range_min: float
    price_range_max: float


class ImageAnalysisResponse(BaseModel):
    detected_brand: str | None
    detected_model: str | None
    detected_body_type: str | None
    detected_color: str | None
    estimated_year: int | None
    vehicle_category: str | None
    images: list[dict]


class DamageAnalysisResponse(BaseModel):
    has_damage: bool
    damage_description: str
    severity: str
    detected_issues: list[str]
    confidence: int
    image_info: dict


class PredictionHistoryItem(BaseModel):
    id: int
    timestamp: str
    oem: str
    model: str
    variant: str
    km: int
    car_age: int
    predicted_price: float


class AppMetadata(BaseModel):
    model_version: str
    brands_count: int
    models_count: int
    total_predictions: int
    dataset_version: str
