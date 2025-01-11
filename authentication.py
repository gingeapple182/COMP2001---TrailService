import requests
from flask import request, jsonify, session
from models import TrailUser, Database

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
SESSION_KEY = "logged_in_user"

def User_Authentication():
    data = request.get_json()
    print(f"Received login data: {data}")
    
    # Validate that email and password are provided
    if not data or "email" not in data or "password" not in data:
        print("Login failed: Missing email or password")
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
            print(f"Parsed external API response: {result}")
            
            if len(result) == 2 and result[0] == "Verified" and result[1] == "True":
                session[SESSION_KEY] = data["email"]
                print(f"Login successful for user: {data['email']}")
                return jsonify({"message": "Login successful", "token": data["email"]}), 200
            else:
                print("Login failed: Invalid credentials")
                return jsonify({"message": "Invalid credentials", "verified": False}), 401
        else:
            print("Login failed: External service error")
            return jsonify({"error": "Failed to authenticate with the external service"}), 500

    except Exception as e:
        print(f"Error during authentication: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


def get_user_role(request):
    user_email = session.get(SESSION_KEY)

    if not user_email:
        print("Authorization failed: Missing header")
        return None
    
    try:
        # Check user role
        user = Database.session.query(TrailUser).filter_by(Email_Address=user_email).first()
        if user:
            print(f"User role found: {user.User_Role} for user {user.Email_Address}")
            return user.User_Role
        else:
            print("Authorization failed: User not found in database")
            return None
        
    except Exception as e:
        print(f"Error retrieving role: {e}")
        return None
