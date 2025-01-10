import requests
from flask import request, jsonify

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def User_Authentication():
    data = request.get_json()
    
    # Validate that email and password are provided
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400
    
    try:
        # Send POST request to the external Authenticator API
        response = requests.post(AUTH_API_URL, json={
            "email": data["email"],
            "password": data["password"]
        })
        
        # Log the response for debugging
        print(f"External API response: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            result = response.json()  # Parse the response as a list
            if len(result) == 2 and result[0] == "Verified" and result[1] == "True":
                return jsonify({"message": "Login successful", "verified": True}), 200
            else:
                return jsonify({"message": "Invalid credentials", "verified": False}), 401
        else:
            return jsonify({"error": "Failed to authenticate with the external service"}), 500

    except Exception as e:
        print(f"Error during authentication: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
