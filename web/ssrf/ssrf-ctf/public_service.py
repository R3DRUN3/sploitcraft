from flask import Flask, request, jsonify
import requests  # <-- Importing requests library

app = Flask(__name__)

@app.route('/fetch', methods=['GET'])
def fetch_url():
    url = request.args.get('url')
    try:
        # Vulnerable to SSRF
        response = requests.get(url)
        return jsonify({"status": "success", "content": response.text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Coming Soon</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
                overflow: hidden;
            }
            h1 {
                font-size: 3em;
                margin: 0;
                padding: 0;
                letter-spacing: 5px;
                text-align: center;
            }
            p {
                font-size: 1.2em;
                text-align: center;
                margin-top: 20px;
            }
            .container {
                text-align: center;
                animation: fadeIn 3s ease-in-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            .wave {
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 15vh;
                background: url('https://svgshare.com/i/_UC.svg') repeat-x;
                background-size: contain;
                animation: wave 8s cubic-bezier(.55,.5,.45,.5) infinite;
            }
            .wave:nth-of-type(2) {
                bottom: 10vh;
                opacity: 0.5;
                animation: wave 4s cubic-bezier(.55,.5,.45,.5) reverse infinite;
            }
            @keyframes wave {
                0% { background-position-x: 0; }
                100% { background-position-x: 1000px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Coming Soon</h1>
            <p>We are working for ya!</p>
        </div>
        <div class="wave"></div>
        <div class="wave"></div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
