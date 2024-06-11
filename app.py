from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///steganography.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()

def embed_message(image_path, message, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()
    message += chr(0)
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    message_index = 0
    for y in range(img.height):
        for x in range(img.width):
            if message_index < len(binary_message):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary_message[message_index])
                pixels[x, y] = (r, g, b)
                message_index += 1
    img.save(output_path)

def extract_message(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()
    binary_message = ''
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '00000000':
            break
        message += chr(int(byte, 2))
    return message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/encode', methods=['POST'])
def encode():
    if 'image' not in request.files or 'message' not in request.form:
        return jsonify({'error': 'Invalid input'}), 400
    image = request.files['image']
    message = request.form['message']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(image.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    image.save(input_path)
    embed_message(input_path, message, output_path)
    new_image_data = ImageData(filename=filename, message=message)
    db.session.add(new_image_data)
    db.session.commit()
    return jsonify({'filename': filename})

@app.route('/api/decode', methods=['POST'])
def decode():
    if 'image' not in request.files:
        return jsonify({'error': 'Invalid input'}), 400
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(image.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(input_path)
    message = extract_message(input_path)
    return jsonify({'message': message})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
