import os
import shutil
import zipfile
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

user_home = os.path.expanduser("~")
cindut_folder = os.path.join(user_home, "Downloads", "cindut")

def check_exist_cindut():
    if not os.path.exists(cindut_folder):
        os.makedirs(cindut_folder)

@app.route('/zip', methods=['POST'])
def process_zip():
    check_exist_cindut()

    if (os.path.exists("RJ")):
        shutil.rmtree("RJ")
        
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    requestanNama = request.form["filename"] + ".pdf"
    requestanNamaZip = request.form["zipname"] + ".zip"

    if file.filename == '':
        return "No selected file", 400

    if file:
        zip_filename = secure_filename(file.filename)
        zip_filepath = os.path.join(cindut_folder, zip_filename)
        file.save(zip_filepath)

        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall("RJ")

        output_zip_filepath = os.path.join(cindut_folder, requestanNamaZip)
        with zipfile.ZipFile(output_zip_filepath, 'w') as output_zip:
            for root, _, files in os.walk("RJ"):
                for filename in files:
                    if filename == requestanNama:
                        pdf_path = os.path.join(root, filename)
                        output_zip.write(pdf_path, os.path.relpath(pdf_path, "RJ"))

        output_extracted_folder = os.path.join(cindut_folder, requestanNama[:-4])
        with zipfile.ZipFile(output_zip_filepath, 'r') as output_zip:
            output_zip.extractall(output_extracted_folder)
        
        return jsonify({"message": "PDFs processed successfully!"})

if __name__ == "__main__":
    check_exist_cindut()
    app.run(debug=True)
