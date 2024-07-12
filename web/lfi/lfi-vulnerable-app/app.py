from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>LFI Demo</title>
        </head>
        <body>
            <h1>LFI PoC</h1>
            <form action="/view" method="get">
                <label for="file">File:</label>
                <input type="text" id="file" name="file">
                <input type="submit" value="View File">
            </form>
        </body>
        </html>
    '''

@app.route('/view')
def view_file():
    file = request.args.get('file', '')
    if file:
        try:
            # Simple LFI vulnerability demonstration
            return send_file(os.path.join('.', file))
        except Exception as e:
            return str(e)
    else:
        return "No file specified."

if __name__ == '__main__':
    app.run(debug=True)
