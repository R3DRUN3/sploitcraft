from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def index():
    url = request.args.get('url', '')
    response_content = ''
    if url:
        try:
            response = requests.get(url)
            response_content = response.text
        except requests.RequestException as e:
            response_content = f"Error fetching URL: {e}"
    
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SSRF Demo</title>
        </head>
        <body>
            <h1>SSRF PoC</h1>
            <form action="" method="get">
                <label for="url">URL:</label>
                <input type="text" id="url" name="url">
                <input type="submit" value="Fetch">
            </form>
            <div>
                <h2>Response Content:</h2>
                <pre>{{ response_content | safe }}</pre>
            </div>
        </body>
        </html>
    ''', response_content=response_content)

if __name__ == '__main__':
    app.run(debug=True)