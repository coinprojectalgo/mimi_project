"""
Authentication Module — Handles login, signup, and logout via Supabase Auth.
"""
import streamlit as st
from supabase import create_client
import config


def get_supabase_client():
    """Initialize and return Supabase client."""
    return create_client(config.SUPABASE_URL, config.SUPABASE_KEY)


def sign_up(email: str, password: str, full_name: str, phone: str = "",
            farm_location: str = "", latitude: float = None, longitude: float = None) -> dict:
    """
    Register a new user with Supabase Auth and create their profile.

    Returns:
        dict with 'success' (bool), 'message' (str), and optionally 'user' data.
    """
    try:
        supabase = get_supabase_client()

        metadata = {
            "full_name": full_name,
            "phone": phone,
            "farm_location": farm_location,
            "latitude": latitude,
            "longitude": longitude,
        }

        # Create auth user with metadata
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": metadata
            }
        })

        if response.user:
            # If session is provided immediately (auto-confirm enabled)
            if response.session and response.session.access_token:
                supabase.postgrest.auth(response.session.access_token)

            # Try to create profile record
            profile_data = {
                "id": response.user.id,
                "full_name": full_name,
                "phone": phone,
                "farm_location": farm_location,
            }
            if latitude is not None:
                profile_data["latitude"] = latitude
            if longitude is not None:
                profile_data["longitude"] = longitude

            try:
                supabase.table("profiles").upsert(profile_data).execute()
            except Exception as pe:
                # Log error but don't fail registration if profile insert fails due to RLS prior to confirmation
                print(f"Profile insert deferred: {pe}")

            return {
                "success": True,
                "message": "Account created successfully! You can now log in.",
                "user": response.user
            }
        else:
            return {
                "success": False,
                "message": "Sign up failed. Please try again."
            }

    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg.lower() or "already been registered" in error_msg.lower():
            return {"success": False, "message": "This email is already registered. Please log in instead."}
        elif "password" in error_msg.lower():
            return {"success": False, "message": "Password must be at least 6 characters long."}
        elif "rate limit" in error_msg.lower():
            return {
                "success": False,
                "message": (
                    "⚠️ Supabase Email Rate Limit Exceeded (default: 3 confirmation emails/hour on free tier).\n\n"
                    "👉 To fix this immediately: In your Supabase Dashboard, go to Authentication → Providers → Email, "
                    "turn OFF 'Confirm email', and click Save. This removes confirmation emails and allows unlimited instant registrations."
                )
            }
        return {"success": False, "message": f"Error: {error_msg}"}


def sign_in(email: str, password: str) -> dict:
    """
    Log in an existing user.

    Returns:
        dict with 'success' (bool), 'message' (str), and optionally 'user' and 'session' data.
    """
    try:
        supabase = get_supabase_client()

        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if response.user and response.session:
            # Authenticate postgrest client with user access token
            supabase.postgrest.auth(response.session.access_token)

            # Fetch profile
            profile = supabase.table("profiles") \
                .select("*") \
                .eq("id", response.user.id) \
                .execute()

            profile_data = profile.data[0] if (profile.data and len(profile.data) > 0) else None

            # If profile not found, populate it from user_metadata
            if not profile_data:
                meta = response.user.user_metadata or {}
                profile_data = {
                    "id": response.user.id,
                    "full_name": meta.get("full_name", email.split("@")[0]),
                    "phone": meta.get("phone", ""),
                    "farm_location": meta.get("farm_location", ""),
                }
                if meta.get("latitude") is not None:
                    profile_data["latitude"] = meta.get("latitude")
                if meta.get("longitude") is not None:
                    profile_data["longitude"] = meta.get("longitude")
                try:
                    p_res = supabase.table("profiles").upsert(profile_data).execute()
                    if p_res.data:
                        profile_data = p_res.data[0]
                except Exception as pe:
                    print(f"Profile auto-creation on login: {pe}")

            return {
                "success": True,
                "message": "Logged in successfully!",
                "user": response.user,
                "session": response.session,
                "profile": profile_data or {}
            }
        else:
            return {"success": False, "message": "Invalid email or password."}

    except Exception as e:
        error_msg = str(e)
        if "invalid" in error_msg.lower() or "credentials" in error_msg.lower():
            return {"success": False, "message": "Invalid email or password. Please try again."}
        if "email not confirmed" in error_msg.lower():
            return {"success": False, "message": "Please verify your email before logging in. Check your inbox."}
        return {"success": False, "message": f"Login error: {error_msg}"}


def sign_out():
    """Log out the current user and clear session state."""
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
    except Exception:
        pass  # Even if sign_out fails server-side, clear local session

    # Clear all session state
    keys_to_clear = [
        "authenticated", "user", "session", "profile",
        "access_token", "user_id", "user_name", "user_email"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def init_session(user, session, profile: dict):
    """Initialize session state after successful login."""
    st.session_state["authenticated"] = True
    st.session_state["user"] = user
    st.session_state["session"] = session
    st.session_state["profile"] = profile
    st.session_state["access_token"] = session.access_token
    st.session_state["user_id"] = user.id
    st.session_state["user_email"] = user.email
    st.session_state["user_name"] = profile.get("full_name", user.email.split("@")[0])


def is_authenticated() -> bool:
    """Check if the current user is authenticated."""
    return st.session_state.get("authenticated", False)


def get_current_user_id() -> str:
    """Get the current authenticated user's ID."""
    return st.session_state.get("user_id", "")


def get_current_profile() -> dict:
    """Get the current user's profile data."""
    return st.session_state.get("profile", {})
