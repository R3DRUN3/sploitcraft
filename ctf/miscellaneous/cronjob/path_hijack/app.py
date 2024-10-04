from flask import Flask, request, send_from_directory, jsonify, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    # List files in the uploads directory
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CTF Upload Challenge</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: #fff;
                padding: 30px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                width: 500px;
                text-align: center;
                position: relative;
            }
            h1 {
                color: #333;
                font-size: 28px;
            }
            input[type="file"] {
                margin: 15px 0;
                width: 100%;
                padding: 10px;
            }
            input[type="submit"] {
                background-color: #28a745;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            input[type="submit"]:hover {
                background-color: #218838;
            }
            .file-list {
                margin-top: 30px;
                text-align: left;
                width: 100%;
            }
            .file-list ul {
                list-style-type: none;
                padding: 0;
            }
            .file-list li {
                background-color: #f9f9f9;
                margin: 5px 0;
                padding: 10px;
                border-radius: 4px;
            }
            .help-icon {
                position: absolute;
                top: 10px;
                right: 10px;
                font-size: 24px;
                cursor: pointer;
                color: #007bff;
            }
            .help-modal {
                display: none;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: white;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                border-radius: 8px;
                z-index: 100;
            }
            .help-modal h2 {
                font-size: 18px;
                margin-bottom: 10px;
            }
            .close-help {
                position: absolute;
                top: 10px;
                right: 10px;
                cursor: pointer;
                font-size: 20px;
                color: #999;
            }
            .modal {
                display: none;
                position: fixed;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                background-color: #fff;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                border-radius: 10px;
                z-index: 200;
            }
            .modal h2 {
                margin: 0 0 10px;
            }
            .modal p {
                margin: 0 0 10px;
            }
            .modal button {
                background-color: #28a745;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .modal button:hover {
                background-color: #218838;
            }
        </style>
        <script>
            function toggleHelp() {
                var helpModal = document.getElementById('helpModal');
                helpModal.style.display = helpModal.style.display === 'block' ? 'none' : 'block';
            }

            function closeUploadModal() {
                document.getElementById('uploadModal').style.display = 'none';
            }

            function uploadFile() {
                var formData = new FormData(document.getElementById('uploadForm'));
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/upload', true);

                xhr.onload = function() {
                    if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        var modal = document.getElementById('uploadModal');
                        var filePathText = document.getElementById('filePath');
                        filePathText.textContent = response.filepath;
                        modal.style.display = 'block';
                    }
                };

                xhr.send(formData);
                return false;
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Upload Your File</h1>
            <form id="uploadForm" onsubmit="return uploadFile()" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <input type="submit" value="Upload">
                <span class="help-icon" onclick="toggleHelp()">❓</span>
            </form>
            <div class="file-list">
                <h2>Uploaded Files:</h2>
                <ul>
                {% for file in files %}
                    <li><a href="/uploads/{{ file }}">{{ file }}</a></li>
                {% endfor %}
                </ul>
            </div>
        </div>

        <!-- Help Modal -->
        <div class="help-modal" id="helpModal">
            <span class="close-help" onclick="toggleHelp()">✖</span>
            <h2>Clue</h2>
            <p>This upload service runs a <b>Cron job</b> every minute. The Cron job runs <code>ls</code> and other binaries in order to push the list of uploaded file to a backend service, but there's a <i>misconfiguration</i>. The Cron job is using an incorrect <b>PATH</b>, meaning it could be tricked to run something else...</p>
        </div>

        <!-- Upload Confirmation Modal -->
        <div class="modal" id="uploadModal">
            <h2>File Uploaded Successfully</h2>
            <p>Your file was uploaded to the following path:</p>
            <p id="filePath"></p>
            <button onclick="closeUploadModal()">Close</button>
        </div>

    </body>
    </html>
    ''', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({'filepath': filepath})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5023)
