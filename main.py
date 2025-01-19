import requests
from flask import Flask, request, jsonify

# Flask app initialization
app = Flask(__name__)

# API Key and Endpoint
GOOGLE_API_KEY = "AIzaSyC2wxR3SyQ5qEDzq6vrO7keM4p4mowOy5o"
GOOGLE_API_ENDPOINT = "https://language.googleapis.com/v1/documents:analyzeEntities"

# Function to analyze user preferences using Google NLP API
def analyze_preferences(user_input):
    headers = {"Content-Type": "application/json"}
    data = {
        "document": {
            "type": "PLAIN_TEXT",
            "content": user_input
        },
        "encodingType": "UTF8"
    }

    try:
        response = requests.post(
            f"{GOOGLE_API_ENDPOINT}?key={GOOGLE_API_KEY}",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error with Google NLP API: {e}")
        return {"error": "Failed to analyze preferences"}

# Function to fetch gift suggestions (mock implementation)
def search_gifts(preferences):
    # Example: use preferences to refine product results
    # Replace with integration to a real product API
    products = [
        {"title": "Personalized Mug", "price": "$15.00", "url": "https://example.com/mug"},
        {"title": "Bluetooth Speaker", "price": "$45.00", "url": "https://example.com/speaker"},
        {"title": "Handmade Journal", "price": "$25.00", "url": "https://example.com/journal"},
    ]
    return products

# Flask route for suggesting gifts
@app.route('/suggest-gift', methods=['POST'])
def suggest_gift():
    # Parse user input from the request
    data = request.json
    user_input = data.get("user_input", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Analyze user preferences using Google NLP API
    preferences = analyze_preferences(user_input)
    if "error" in preferences:
        return jsonify({"error": "Failed to analyze preferences"}), 500

    # Fetch gift suggestions based on preferences
    gift_suggestions = search_gifts(preferences)

    return jsonify({"suggestions": gift_suggestions})

# Example usage (for testing locally)
if __name__ == '__main__':
    app.run(debug=True)
