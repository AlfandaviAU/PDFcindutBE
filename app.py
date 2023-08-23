from flask import Flask, request, render_template, jsonify
from PyPDF2 import PdfMerger
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

user_home = os.path.expanduser("~")
cindut_folder = os.path.join(user_home, "Downloads", "cindut")

def check_exist_cindut():
    if not os.path.exists(cindut_folder):
        os.makedirs(cindut_folder)

UPLOAD_FOLDER = cindut_folder

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_files():
    check_exist_cindut()

    files = request.files.getlist('file')
    uploaded_file_paths = []

    for file in files:
        if file.filename == '':
            return "No selected file"
        if file and file.filename.endswith('.pdf'):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            uploaded_file_paths.append(filename)

    return jsonify({"message": "Files uploaded successfully"})

@app.route("/filename", methods=["GET"])
def get_filenames():
    check_exist_cindut()
    filenames = [filename for filename in os.listdir(app.config['UPLOAD_FOLDER']) if filename.endswith('.pdf')]
    return jsonify({"filenames": filenames})


@app.route('/merge', methods=['POST'])
def merge_pdfs():
    check_exist_cindut()
    data = request.get_json()
    pdf_files = data.get('pdf_files', [])   
    pdf_name = data.get('pdf_name')

    if (pdf_name == ""):
        pdf_name = "merged"

    if not pdf_files:
        return jsonify({"message": "No PDF files provided"}), 400
    
    merger = PdfMerger()
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file)
        merger.append(pdf_path)

    merged_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], (pdf_name+".pdf"))
    merger.write(merged_pdf_path)
    merger.close()

    for pdf_path in pdf_files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], pdf_path))

    return jsonify({"message": f"Merged PDF created: {merged_pdf_path} and uploaded PDFs deleted."})

@app.route('/delete', methods=['DELETE'])
def delete_file():
    check_exist_cindut()
    data = request.get_json()
    filename = data.get('filename')

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": f"File '{filename}' deleted."})
    else:
        return jsonify({"message": f"File '{filename}' not found."}), 404



if __name__ == '__main__':
    app.run(debug=True)
