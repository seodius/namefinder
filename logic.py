import json
import whois
from google import genai
from google.genai import types
import config
import os

def _get_client():
    """Initializes and returns the GenAI client, checking for a valid API key."""
    api_key = config.GEMINI_API_KEY
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        raise ValueError("Gemini API key is not set or is still the placeholder value in config.py.")
    return genai.Client(api_key=api_key)

def generate_uvp(data):
    """Generates a Unique Value Proposition using the new GenAI SDK."""
    client = _get_client()

    user_prompt = f"""
    Here is the user's input:
    - Headline: {data.get('headline')}
    - What is it?: {data.get('what')}
    - Who is it for?: {data.get('forWho')}
    - Key Features: {data.get('features')}
    """

    full_prompt = f"{config.UVP_SYSTEM_PROMPT}\n\n{user_prompt}"

    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=full_prompt
    )
    return response.text.strip()

def generate_lexicon(data):
    """Generates a lexicon using the new GenAI SDK."""
    client = _get_client()

    user_prompt = f"""
    Here is the user's input:
    - Unique Value Proposition: {data.get('uvp')}
    - Headline: {data.get('headline')}
    - Target Audience: {data.get('forWho')}
    - Key Features: {data.get('features')}
    """

    full_prompt = f"{config.LEXICON_SYSTEM_PROMPT}\n\n{user_prompt}"

    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=full_prompt,
        config={'response_mime_type': 'application/json'}
    )

    # The new SDK might handle JSON parsing better, but for now, we'll parse the text.
    cleaned_text = response.text.strip()
    return json.loads(cleaned_text)

def generate_and_check_names(data):
    """Generates names, checks domain availability, and returns a curated list."""
    client = _get_client()
    selected_lexicon_str = ", ".join([item['word'] for item in data.get('lexicon', [])])

    user_prompt = f"""
    Here is the user's input:
    - Unique Value Proposition: {data.get('uvp')}
    - Headline: {data.get('headline')}
    - Target Audience: {data.get('forWho')}
    - Key Features: {data.get('features')}
    - Curated Lexicon: {selected_lexicon_str}
    """

    full_prompt = f"{config.NAMES_SYSTEM_PROMPT}\n\n{user_prompt}"

    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=full_prompt,
        config={'response_mime_type': 'application/json'}
    )

    cleaned_text = response.text.strip()
    suggested_names = json.loads(cleaned_text)

    curated_list = []
    for name_info in suggested_names:
        name = name_info.get("name")
        if not name:
            continue

        domain_name = f"{name.replace(' ', '').lower()}.com"
        try:
            w = whois.whois(domain_name)
            is_available = not bool(w.domain_name)
        except whois.parser.PywhoisError:
            is_available = True
        except Exception as e:
            print(f"Error checking domain {domain_name}: {e}")
            is_available = False

        curated_list.append({
            "name": name,
            "competitors": name_info.get("competitors", "N/A"),
            "domainAvailable": is_available
        })

    return curated_list
