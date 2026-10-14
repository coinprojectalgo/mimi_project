"""
LLM Engine — Integrates NVIDIA's meta/muse-glimmer-30b LLM with RAG pipeline.

Takes inputs from:
1. Image model prediction
2. Farmer-provided data
3. Environment & soil data
4. Location-based nearby disease alerts
5. RAG knowledge base context

Returns a comprehensive diagnosis with confidence, risk level, and remedies.
"""
import json
from openai import OpenAI
import config
from knowledge_base import build_rag_context


SYSTEM_PROMPT = """You are an expert agricultural scientist and plant pathologist AI assistant. You specialize in crop disease diagnosis, risk assessment, and providing actionable remedies to farmers.

You will receive multiple sources of information:
1. **Image Model Prediction**: A CNN model's prediction of the disease from a leaf image, with confidence scores.
2. **Farmer's Observations**: Manual input from the farmer about crop conditions, symptoms, and farming practices.
3. **Environmental & Soil Data**: Temperature, humidity, rainfall, soil pH, NPK levels, etc.
4. **Nearby Disease Alerts**: Recent disease reports from nearby locations (within ~5km radius).
5. **Disease Knowledge Base**: Detailed scientific knowledge about the predicted disease.

Your task is to synthesize ALL this information and provide:

1. **Final Diagnosis**: Confirm, modify, or correct the image model's prediction based on all available evidence.
2. **Confidence Level**: Your confidence in the diagnosis (High/Medium/Low) with explanation.
3. **Risk Level**: Overall risk to the crop (Low/Medium/High/Critical).
4. **Detailed Analysis**: Why you reached this conclusion, considering environmental factors, nearby outbreaks, and farmer observations.
5. **Remedies & Solutions**: Both organic/natural and chemical treatments, prioritizing the most practical options for the farmer.
6. **Preventive Measures**: Steps to prevent recurrence or spread.
7. **Nearby Alert Impact**: If nearby disease reports are present, assess the regional risk and recommend community-level actions.

IMPORTANT GUIDELINES:
- If the crop appears healthy, still provide preventive care recommendations.
- If farmer observations contradict the image prediction, weigh both carefully and explain.
- Consider environmental conditions — some diseases thrive in specific conditions.
- If nearby locations report the same disease, emphasize urgency and community action.
- Be practical — farmers may not have access to all chemicals. Always include organic alternatives.
- Use simple, clear language that a farmer can understand.
- Structure your response in clear sections with headers.

Respond ONLY with a valid JSON object with these exact keys:
{
    "final_diagnosis": "The confirmed disease name or 'Healthy'",
    "confidence": "High/Medium/Low",
    "confidence_explanation": "Why you are this confident",
    "risk_level": "Low/Medium/High/Critical",
    "risk_explanation": "Why this risk level",
    "detailed_analysis": "Full analysis considering all inputs",
    "organic_remedies": ["remedy 1", "remedy 2", ...],
    "chemical_treatments": ["treatment 1", "treatment 2", ...],
    "preventive_measures": ["measure 1", "measure 2", ...],
    "nearby_alert_assessment": "Assessment of nearby disease impact (or 'No nearby alerts')",
    "immediate_actions": ["action 1", "action 2", ...],
    "additional_notes": "Any extra advice for the farmer"
}"""


def _build_user_prompt(
    prediction: dict,
    farmer_inputs: dict,
    environment_data: dict,
    nearby_alerts: list,
    rag_context: str,
) -> str:
    """Build a comprehensive prompt from all data sources."""

    parts = []

    # 1. Image Model Prediction
    parts.append("## 1. IMAGE MODEL PREDICTION")
    parts.append(f"- Predicted Disease: {prediction.get('predicted_class', 'Unknown')}")
    parts.append(f"- Model Confidence: {prediction.get('confidence', 0):.1f}%")
    if prediction.get("top3"):
        parts.append("- Top 3 Predictions:")
        for item in prediction["top3"]:
            parts.append(f"  • {item['class']}: {item['probability']:.1f}%")

    # 2. Farmer Inputs
    parts.append("\n## 2. FARMER OBSERVATIONS")
    farmer_fields = {
        "crop_type": "Crop Type",
        "crop_variety": "Crop Variety",
        "growth_stage": "Growth Stage",
        "visible_symptoms": "Visible Symptoms Described",
        "irrigation_type": "Irrigation Type",
        "fertilizer_history": "Fertilizer History",
        "pesticide_use": "Pesticide Usage",
        "pest_presence": "Pest Presence Noted",
    }
    for key, label in farmer_fields.items():
        value = farmer_inputs.get(key, "")
        if value:
            parts.append(f"- {label}: {value}")

    # 3. Environment & Soil Data
    parts.append("\n## 3. ENVIRONMENTAL & SOIL CONDITIONS")
    env_fields = {
        "temperature": ("Temperature", "°C"),
        "humidity": ("Humidity", "%"),
        "rainfall": ("Recent Rainfall", "mm"),
        "soil_moisture": ("Soil Moisture", "%"),
        "soil_ph": ("Soil pH", ""),
        "nitrogen": ("Nitrogen (N)", "kg/ha"),
        "phosphorus": ("Phosphorus (P)", "kg/ha"),
        "potassium": ("Potassium (K)", "kg/ha"),
    }
    has_env_data = False
    for key, (label, unit) in env_fields.items():
        value = environment_data.get(key)
        if value is not None and value != "":
            parts.append(f"- {label}: {value}{unit}")
            has_env_data = True
    if not has_env_data:
        parts.append("- No environmental data provided")

    # 4. Nearby Disease Alerts
    parts.append("\n## 4. NEARBY DISEASE ALERTS (within 5km radius, last 30 days)")
    if nearby_alerts:
        parts.append(f"⚠️ {len(nearby_alerts)} disease report(s) found nearby:")
        for alert in nearby_alerts[:10]:  # Limit to 10 alerts
            dist = alert.get("distance_km", "?")
            disease = alert.get("predicted_disease", "Unknown")
            confidence = alert.get("model_confidence", 0)
            risk = alert.get("risk_level", "Unknown")
            date = alert.get("created_at", "Unknown")
            parts.append(f"  • {disease} (confidence: {confidence:.0f}%, risk: {risk}) — {dist:.1f}km away — reported: {date}")
    else:
        parts.append("- No recent disease reports found in the nearby area.")

    # 5. RAG Knowledge Base Context
    parts.append(f"\n## 5. DISEASE KNOWLEDGE BASE\n{rag_context}")

    return "\n".join(parts)


def analyze_with_llm(
    prediction: dict,
    farmer_inputs: dict = None,
    environment_data: dict = None,
    nearby_alerts: list = None,
) -> dict:
    """
    Run the full LLM analysis pipeline.

    Args:
        prediction: dict from image_model.predict()
        farmer_inputs: dict with crop_type, symptoms, etc.
        environment_data: dict with temperature, humidity, soil data, etc.
        nearby_alerts: list of nearby disease reports from database

    Returns:
        dict with LLM analysis results
    """
    if farmer_inputs is None:
        farmer_inputs = {}
    if environment_data is None:
        environment_data = {}
    if nearby_alerts is None:
        nearby_alerts = []

    # Build RAG context from knowledge base
    predicted_disease = prediction.get("predicted_class", "")
    crop_type = farmer_inputs.get("crop_type", "")
    rag_context = build_rag_context(predicted_disease, crop_type)

    # Build comprehensive prompt
    user_prompt = _build_user_prompt(
        prediction=prediction,
        farmer_inputs=farmer_inputs,
        environment_data=environment_data,
        nearby_alerts=nearby_alerts,
        rag_context=rag_context,
    )

    try:
        # Call NVIDIA LLM API
        client = OpenAI(
            base_url=config.NVIDIA_BASE_URL,
            api_key=config.NVIDIA_API_KEY,
        )

        completion = client.chat.completions.create(
            model=config.NVIDIA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            top_p=0.9,
            max_tokens=config.MAX_LLM_TOKENS,
            stream=False,
        )

        msg = completion.choices[0].message
        response_text = (msg.content or getattr(msg, "reasoning_content", "") or "").strip()

        # Extract JSON from response (handling markdown fences or surrounding chatter)
        json_str = response_text
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        elif "{" in json_str and "}" in json_str:
            start_idx = json_str.find("{")
            end_idx = json_str.rfind("}") + 1
            json_str = json_str[start_idx:end_idx].strip()

        result = json.loads(json_str)

        # Ensure all required keys exist
        required_keys = [
            "final_diagnosis", "confidence", "confidence_explanation",
            "risk_level", "risk_explanation", "detailed_analysis",
            "organic_remedies", "chemical_treatments", "preventive_measures",
            "nearby_alert_assessment", "immediate_actions", "additional_notes"
        ]
        for key in required_keys:
            if key not in result:
                result[key] = "Not available"

        result["success"] = True
        return result

    except json.JSONDecodeError:
        # If JSON parsing fails, return raw text in a structured format
        return {
            "success": True,
            "final_diagnosis": prediction.get("predicted_class", "Unknown"),
            "confidence": "Medium",
            "confidence_explanation": "Based on image model prediction. LLM response could not be parsed.",
            "risk_level": "Medium",
            "risk_explanation": "Unable to fully assess — using model prediction as baseline.",
            "detailed_analysis": response_text if 'response_text' in dir() else "Analysis could not be completed.",
            "organic_remedies": ["Please consult a local agricultural extension officer."],
            "chemical_treatments": ["Please consult a local agricultural extension officer."],
            "preventive_measures": ["Monitor crop regularly.", "Maintain good farm hygiene."],
            "nearby_alert_assessment": "Unable to assess.",
            "immediate_actions": ["Take more photos for confirmation.", "Contact local agri-office."],
            "additional_notes": "The AI analysis encountered an issue. Please consult an expert."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "final_diagnosis": prediction.get("predicted_class", "Unknown"),
            "confidence": "Low",
            "confidence_explanation": f"LLM analysis failed: {str(e)}",
            "risk_level": "Unknown",
            "risk_explanation": "Could not complete analysis.",
            "detailed_analysis": f"Error during LLM analysis: {str(e)}. Falling back to image model prediction only.",
            "organic_remedies": ["Consult local agricultural extension officer for detailed recommendations."],
            "chemical_treatments": ["Consult local agricultural extension officer for detailed recommendations."],
            "preventive_measures": ["Monitor crop closely.", "Take additional photos."],
            "nearby_alert_assessment": "Unable to assess due to error.",
            "immediate_actions": ["Isolate affected plants if possible.", "Seek expert opinion."],
            "additional_notes": "The analysis encountered an error. The image model prediction is shown as a baseline."
        }
