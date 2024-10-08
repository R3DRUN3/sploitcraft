from flask import Flask, request, Response

app = Flask(__name__)

# Basic authentication credentials
USERNAME = 'admin'
PASSWORD = 'monkey'

def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return username == USERNAME and password == PASSWORD

def authenticate():
    """Sends a 401 response that prompts for basic auth with a custom message."""
    return Response('Unauthorized, you need to authenticate as admin', 401, 
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/')
def index():
    # Check for Basic Auth credentials
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()  # Return 401 with custom message

    return "Congratulations! You've pivoted through SSRF. Here's the final part of your flag: c3sfv1l_!!}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21074)
