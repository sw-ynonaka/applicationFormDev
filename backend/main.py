from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import fitz  # PyMuPDF
import requests
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

def download_font(url, save_path):
    response = requests.get(url)
    response.raise_for_status()  # エラーチェック
    with open(save_path, 'wb') as f:
        f.write(response.content)

def find_blank_position(page, search_text, text_length):
    text_instances = page.search_for(search_text)
    if text_instances:
        x0, y0, x1, y1 = text_instances[0]
        return x1 + 5 + text_length * 5, y0 + (y1 - y0) / 2
    else:
        raise ValueError(f"'{search_text}' not found in the PDF.")

def add_text_to_pdf(pdf_path, text, output_path, font_path, position):
    doc = fitz.open(pdf_path)
    page = doc[0]
    x, y = position
    page.insert_text((x, y), text, fontsize=12, fontfile=font_path, color=(0, 0, 0))
    doc.save(output_path)

@app.route('/update-pdf', methods=['POST'])
def update_pdf():
    data = request.json
    pdf_url = data['pdf_url']
    text = data['text']
    font_url = data['font_url']
    search_text = data['search_text']
    
    pdf_path = 'temp.pdf'
    font_path = 'temp_font.ttf'
    output_path = 'output.pdf'
    
    try:
        # PDFとフォントをダウンロード
        download_font(pdf_url, pdf_path)
        download_font(font_url, font_path)
        
        # PDFを開いて位置を特定
        doc = fitz.open(pdf_path)
        page = doc[0]
        position = find_blank_position(page, search_text, len(text))
        
        # テキストをPDFに追加
        add_text_to_pdf(pdf_path, text, output_path, font_path, position)
        
        return jsonify({"message": "PDF updated successfully", "output_path": output_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/download-pdf', methods=['GET'])
def download_pdf():
    output_path = 'output.pdf'
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'assets'), filename)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)