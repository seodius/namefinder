from flask import Flask, request, jsonify
from flask_cors import CORS
import logic

app = Flask(__name__)
CORS(app)

@app.route('/api/uvp', methods=['POST'])
def get_uvp():
    try:
        data = request.get_json()
        uvp = logic.generate_uvp(data)
        return jsonify({"uvp": uvp})
    except Exception as e:
        print(f"Error in /api/uvp endpoint: {e}")
        return jsonify({"error": "An error occurred while generating the UVP."}), 500

@app.route('/api/lexicon', methods=['POST'])
def get_lexicon():
    try:
        data = request.get_json()
        lexicon = logic.generate_lexicon(data)
        return jsonify({"lexicon": lexicon})
    except Exception as e:
        print(f"Error in /api/lexicon endpoint: {e}")
        return jsonify({"error": "An error occurred while generating the lexicon."}), 500

@app.route('/api/names', methods=['POST'])
def get_names():
    try:
        data = request.get_json()
        names = logic.generate_and_check_names(data)
        return jsonify({"names": names})
    except Exception as e:
        print(f"Error in /api/names endpoint: {e}")
        return jsonify({"error": "An error occurred while generating names."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
