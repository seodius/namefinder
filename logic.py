import json
import whois
import google.generativeai as genai
import config

# Configure the Gemini API
if config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY" or not config.GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set in config.py. API calls will fail.")
else:
    genai.configure(api_key=config.GEMINI_API_KEY)

def generate_uvp(data):
    """Generates a Unique Value Proposition using the Gemini API."""
    if not genai.api_key:
        raise ValueError("Gemini API key is not configured.")

    user_prompt = f"""
    Here is the user's input:
    - Headline: {data.get('headline')}
    - What is it?: {data.get('what')}
    - Who is it for?: {data.get('forWho')}
    - Key Features: {data.get('features')}
    """

    full_prompt = f"{config.UVP_SYSTEM_PROMPT}\n\n{user_prompt}"

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(full_prompt)
    return response.text.strip()

def generate_lexicon(data):
    """Generates a lexicon using the Gemini API."""
    if not genai.api_key:
        raise ValueError("Gemini API key is not configured.")

    user_prompt = f"""
    Here is the user's input:
    - Unique Value Proposition: {data.get('uvp')}
    - Headline: {data.get('headline')}
    - Target Audience: {data.get('forWho')}
    - Key Features: {data.get('features')}
    """

    full_prompt = f"{config.LEXICON_SYSTEM_PROMPT}\n\n{user_prompt}"

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(full_prompt)

    cleaned_text = response.text.strip()
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:]
    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]

    return json.loads(cleaned_text)

def generate_and_check_names(data):
    """Generates names, checks domain availability, and returns a curated list."""
    if not genai.api_key:
        raise ValueError("Gemini API key is not configured.")

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

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(full_prompt)

    cleaned_text = response.text.strip().replace("```json", "").replace("```", "").strip()
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
