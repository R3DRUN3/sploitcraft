from flask import Flask, redirect, url_for, session, request, render_template
from authlib.integrations.flask_client import OAuth
import os
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration for OAuth
app.config["GOOGLE_CLIENT_ID"] = "<YOUR-CLIENT-ID>"  
app.config["GOOGLE_CLIENT_SECRET"] = "<YOUR-CLIENT-SECRET>" 
app.config["GOOGLE_DISCOVERY_URL"] = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    server_metadata_url=app.config["GOOGLE_DISCOVERY_URL"],
    client_kwargs={"scope": "openid email profile"},
)

# Registered redirect URIs (for proper implementation)
ALLOWED_REDIRECT_URIS = ["http://localhost:5000/dashboard"]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    # Official secure OAuth flow
    nonce = str(uuid.uuid4())
    session["oauth_nonce"] = nonce
    return google.authorize_redirect(
        url_for("auth", _external=True),
        state=nonce,
        nonce=nonce
    )


@app.route("/vulnerable-login")
def vulnerable_login():
    # Vulnerable OAuth flow
    redirect_uri = request.args.get("redirect_uri", url_for("auth", _external=True))
    print(f"Vulnerable redirect to: {redirect_uri}")
    nonce = str(uuid.uuid4())
    session["oauth_nonce"] = nonce
    return google.authorize_redirect(
        redirect_uri,
        state=nonce,
        nonce=nonce
    )


@app.route("/auth")
def auth():
    try:
        # Retrieve the state and session nonce
        state = request.args.get("state")
        session_nonce = session.pop("oauth_nonce", None)

        # Validate state matches session nonce
        if not session_nonce or state != session_nonce:
            raise ValueError("Invalid state or nonce")

        # Retrieve the OAuth token
        token = google.authorize_access_token()

        # Parse the ID token, including nonce verification
        user_info = google.parse_id_token(token, nonce=session_nonce)

        # Debugging: Print user info to logs
        print("User Info:", user_info)

        # Save user information in the session
        session["user"] = user_info
        print("Session Nonce:", session_nonce)
        print("State from Request:", state)
        print("ID Token Nonce (decoded):", token.get("id_token"))  # Decoded for inspection

    except Exception as e:
        # Debugging: Log the error details
        print("Error during authentication:", e)
        return render_template("error.html", message="Authentication failed.")
    
    # Redirect to dashboard if successful
    return redirect(url_for("dashboard"))






@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    if not user:
        return render_template("error.html", message="User not authenticated. Please log in.")
    return render_template("login.html", user=user)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
