from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name', '')
    template = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SSTI Demo</title>
        </head>
        <body>
            <h1>SSTI PoC</h1>
            <form action="" method="get">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name">
                <input type="submit" value="Submit">
            </form>
            <p>Hello, {name}</p>
        </body>
        </html>
    '''
    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True)
