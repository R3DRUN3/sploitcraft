# internal_service_3.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Congratulations! You've pivoted through SSRF. Here's the second part of your flag: V0t_Svc"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10980)