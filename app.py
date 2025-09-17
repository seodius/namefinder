import json
import whois
import google.generativeai as genai
import config
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure the Gemini API
if config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
    print("Warning: GEMINI_API_KEY is not set in config.py. API calls will fail.")
genai.configure(api_key=config.GEMINI_API_KEY)


@app.route('/api/uvp', methods=['POST'])
def get_uvp():
    if not genai.api_key or genai.api_key == "YOUR_GEMINI_API_KEY":
        return jsonify({"error": "Gemini API key is not configured. Please set it in config.py."}), 500

    data = request.get_json()

    user_prompt = f"""
    Here is the user's input:
    - Headline: {data.get('headline')}
    - What is it?: {data.get('what')}
    - Who is it for?: {data.get('forWho')}
    - Key Features: {data.get('features')}
    """

    full_prompt = f"{config.UVP_SYSTEM_PROMPT}\n\n{user_prompt}"

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(full_prompt)
        uvp = response.text.strip()
        return jsonify({"uvp": uvp})
    except Exception as e:
        print(f"Error calling Gemini API for UVP: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/lexicon', methods=['POST'])
def get_lexicon():
    if not genai.api_key or genai.api_key == "YOUR_GEMINI_API_KEY":
        return jsonify({"error": "Gemini API key is not configured. Please set it in config.py."}), 500

    data = request.get_json()

    user_prompt = f"""
    Here is the user's input:
    - Unique Value Proposition: {data.get('uvp')}
    - Headline: {data.get('headline')}
    - Target Audience: {data.get('forWho')}
    - Key Features: {data.get('features')}
    """

    full_prompt = f"{config.LEXICON_SYSTEM_PROMPT}\n\n{user_prompt}"

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(full_prompt)

        # Clean the response to ensure it's valid JSON
        cleaned_text = response.text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]

        lexicon = json.loads(cleaned_text)
        return jsonify({"lexicon": lexicon})
    except json.JSONDecodeError:
        print(f"Error decoding JSON from Gemini response for Lexicon: {response.text}")
        return jsonify({"error": "Failed to parse lexicon from Gemini API. The format was invalid."}), 500
    except Exception as e:
        print(f"Error calling Gemini API for Lexicon: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/names', methods=['POST'])
def get_names():
    if not genai.api_key or genai.api_key == "YOUR_GEMINI_API_KEY":
        return jsonify({"error": "Gemini API key is not configured. Please set it in config.py."}), 500

    data = request.get_json()

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

    try:
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

        return jsonify({"names": curated_list})

    except json.JSONDecodeError:
        print(f"Error decoding JSON from Gemini response for Names: {response.text}")
        return jsonify({"error": "Failed to parse names from Gemini API. The format was invalid."}), 500
    except Exception as e:
        print(f"Error in name generation process: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
