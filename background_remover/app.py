from flask import Flask, render_template, request, send_from_directory
from rembg import remove 
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/remove-background', methods=['POST'])
def remove_bg():
    image_file = request.files['image']
    input_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    output_path = os.path.join(RESULT_FOLDER, 'output.png')

    image_file.save(input_path)

    with open(input_path, 'rb') as i:
        input_data = i.read()
    output_data = remove(input_data)

    with open(output_path, 'wb') as o:
        o.write(output_data)

    return render_template('index.html', result='/results/output.png')

@app.route('/results/<filename>')
def send_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
