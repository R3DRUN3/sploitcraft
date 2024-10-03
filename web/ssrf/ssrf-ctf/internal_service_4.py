# internal_service_4.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Congratulations! You've pivoted through SSRF. Here's the final part of your flag: c3sfv1l_!!}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21074)