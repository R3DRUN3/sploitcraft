from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>XXE Demo</title>
    </head>
    <body>
        <h1>XXE PoC</h1>
        <form action="/parse-xml" method="post" enctype="text/xml">
            <textarea name="xml_input" rows="10" cols="50"></textarea><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    '''

@app.route('/parse-xml', methods=['POST'])
def parse_xml():
    xml_input = request.data
    try:
        parser = etree.XMLParser(resolve_entities=True)
        tree = etree.fromstring(xml_input, parser)
        response = etree.tostring(tree, pretty_print=True).decode()
    except Exception as e:
        response = str(e)
    return f"<pre>{response}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
