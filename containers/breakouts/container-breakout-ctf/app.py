from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read', methods=['POST'])
def read_file():
    filename = request.form['filename']
    try:
        # Vulnerable to RCE, NEED TO RESTRICT THIS FUNCTIONALITY ASAP!!
        output = subprocess.check_output(f'cat {filename}', shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return render_template('index.html', output=output, filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
