from flask import Flask, request, render_template_string
from markupsafe import Markup

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name', '')
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>XSS Demo</title>
        </head>
        <body>
            <h1>XSS PoC</h1>
            <form action="" method="get">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name">
                <input type="submit" value="Submit">
            </form>
            <p>Hello, {{ name | safe }}!</p>
        </body>
        </html>
    ''', name=Markup(name))

if __name__ == '__main__':
    app.run(debug=True)
