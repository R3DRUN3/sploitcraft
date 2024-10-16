from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

SECRET_KEY = "supersecretkey"  # Secret key used for signing JWTs

# Simulate a login endpoint that issues JWT tokens
@app.route("/login", methods=["POST"])
def login():
    # Normally, you'd authenticate the user here. For demo purposes, we assume success.
    user = request.json.get("user", "guest")
    
    # Create JWT token with 'HS256' algorithm
    token = jwt.encode({"user": user}, SECRET_KEY, algorithm="HS256")
    
    return jsonify({"token": token})

# Protected route requiring valid JWT
@app.route("/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization").split(" ")[1]  # Extract token from "Authorization: Bearer <token>"
    
    try:
        # Decode the JWT token. Vulnerable to 'none' algorithm if signature verification is bypassed.
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256", "none"], options={"verify_signature": False})
        return jsonify({"message": f"Welcome {decoded['user']}, you have access to this protected route!"})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(debug=True)
