# internal_service_2.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Congratulations! You've pivoted through SSRF. Here's the first part of your flag: FLAG{sSrF_p1"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2397)