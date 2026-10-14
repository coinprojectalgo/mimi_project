"""
Configuration loader — reads credentials from .env file.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# NVIDIA LLM
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL = "meta/muse-glimmer-30b"

# App Constants
NEARBY_RADIUS_KM = 5.0
NEARBY_DAYS_BACK = 30
MAX_LLM_TOKENS = 4096
