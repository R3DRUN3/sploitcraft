from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)
# Restrict the allowed files
allowed_files = ['Dockerfile', 'example.txt']
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read', methods=['POST'])
def read_file():
    filename = request.form['filename']
    # The following logic needs to be fixed!
    if 'Dockerfile' not in filename and 'example.txt' not in filename:
        return render_template('index.html', output="File non-existent or insufficient permissions", filename=filename)
    try:
        # Vulnerable to RCE, NEED TO RESTRICT THIS FUNCTIONALITY ASAP!!
        output = subprocess.check_output(f'cat {filename}', shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return render_template('index.html', output=output, filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
