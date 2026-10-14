"""
Database Module — Supabase CRUD operations for disease reports and profiles.
"""
import json
from datetime import datetime
from supabase import create_client
import config


import streamlit as st


def _get_client():
    """Get a Supabase client instance with session token attached if logged in."""
    client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    try:
        token = st.session_state.get("access_token")
        if token:
            client.postgrest.auth(token)
    except Exception:
        pass
    return client


def save_disease_report(
    user_id: str,
    # Image prediction
    predicted_disease: str,
    model_confidence: float,
    top3_predictions: list,
    # Farmer inputs
    crop_type: str = None,
    crop_variety: str = None,
    growth_stage: str = None,
    visible_symptoms: str = None,
    irrigation_type: str = None,
    fertilizer_history: str = None,
    pesticide_use: str = None,
    pest_presence: str = None,
    # Environment & Soil
    temperature: float = None,
    humidity: float = None,
    rainfall: float = None,
    soil_moisture: float = None,
    soil_ph: float = None,
    nitrogen: float = None,
    phosphorus: float = None,
    potassium: float = None,
    # Location
    latitude: float = None,
    longitude: float = None,
    region: str = None,
    # LLM Analysis
    llm_diagnosis: str = None,
    llm_confidence: str = None,
    llm_remedies: str = None,
    risk_level: str = None,
    nearby_alerts: list = None,
    # Image
    image_url: str = None,
) -> dict:
    """Save a complete disease report to Supabase."""
    try:
        supabase = _get_client()

        report_data = {
            "user_id": user_id,
            "predicted_disease": predicted_disease,
            "model_confidence": model_confidence,
            "top3_predictions": json.dumps(top3_predictions) if top3_predictions else None,
            "crop_type": crop_type,
            "crop_variety": crop_variety,
            "growth_stage": growth_stage,
            "visible_symptoms": visible_symptoms,
            "irrigation_type": irrigation_type,
            "fertilizer_history": fertilizer_history,
            "pesticide_use": pesticide_use,
            "pest_presence": pest_presence,
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "soil_moisture": soil_moisture,
            "soil_ph": soil_ph,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "latitude": latitude,
            "longitude": longitude,
            "region": region,
            "llm_diagnosis": llm_diagnosis,
            "llm_confidence": llm_confidence,
            "llm_remedies": llm_remedies,
            "risk_level": risk_level,
            "nearby_alerts": json.dumps(nearby_alerts) if nearby_alerts else None,
            "image_url": image_url,
        }

        # Remove None values so Supabase uses defaults
        report_data = {k: v for k, v in report_data.items() if v is not None}

        response = supabase.table("disease_reports").insert(report_data).execute()
        return {"success": True, "data": response.data}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_user_reports(user_id: str, limit: int = 20) -> list:
    """Fetch recent disease reports for a specific user."""
    try:
        supabase = _get_client()
        response = supabase.table("disease_reports") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        return response.data or []
    except Exception as e:
        print(f"Error fetching reports: {e}")
        return []


def get_nearby_disease_reports(latitude: float, longitude: float,
                                radius_km: float = None, days_back: int = None) -> list:
    """
    Find disease reports within a given radius using the
    Supabase RPC function (Haversine formula).
    """
    if radius_km is None:
        radius_km = config.NEARBY_RADIUS_KM
    if days_back is None:
        days_back = config.NEARBY_DAYS_BACK

    try:
        supabase = _get_client()
        response = supabase.rpc("get_nearby_disease_reports", {
            "user_lat": latitude,
            "user_lon": longitude,
            "radius_km": radius_km,
            "days_back": days_back
        }).execute()
        return response.data or []
    except Exception as e:
        print(f"Error fetching nearby reports: {e}")
        return []


def upload_leaf_image(file_bytes: bytes, filename: str, user_id: str) -> str:
    """
    Upload a leaf image to Supabase Storage.
    Returns the public URL of the uploaded image.
    """
    try:
        supabase = _get_client()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        storage_path = f"{user_id}/{timestamp}_{filename}"

        supabase.storage.from_("leaf-images").upload(
            storage_path,
            file_bytes,
            {"content-type": "image/jpeg"}
        )

        public_url = supabase.storage.from_("leaf-images").get_public_url(storage_path)
        return public_url

    except Exception as e:
        print(f"Error uploading image: {e}")
        return ""


def update_user_profile(user_id: str, updates: dict) -> dict:
    """Update user profile data."""
    try:
        supabase = _get_client()
        response = supabase.table("profiles") \
            .update(updates) \
            .eq("id", user_id) \
            .execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_user_stats(user_id: str) -> dict:
    """Get aggregated statistics for the user's reports."""
    try:
        reports = get_user_reports(user_id, limit=100)

        total_scans = len(reports)
        diseases_found = sum(
            1 for r in reports if "Healthy" not in r.get("predicted_disease", "")
        )
        healthy_scans = total_scans - diseases_found
        high_risk = sum(
            1 for r in reports if r.get("risk_level") in ("High", "Critical")
        )

        # Recent diseases
        recent_diseases = []
        for r in reports[:5]:
            if "Healthy" not in r.get("predicted_disease", ""):
                recent_diseases.append({
                    "disease": r.get("predicted_disease"),
                    "confidence": r.get("model_confidence"),
                    "risk": r.get("risk_level"),
                    "date": r.get("created_at"),
                })

        return {
            "total_scans": total_scans,
            "diseases_found": diseases_found,
            "healthy_scans": healthy_scans,
            "high_risk_alerts": high_risk,
            "recent_diseases": recent_diseases,
        }

    except Exception:
        return {
            "total_scans": 0, "diseases_found": 0,
            "healthy_scans": 0, "high_risk_alerts": 0,
            "recent_diseases": []
        }
