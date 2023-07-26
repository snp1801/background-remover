from flask import Flask, request, jsonify, Response
from rembg import remove
from PIL import Image
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

def bgRemove(input_image):
    input_image = Image.open(input_image)
    output_image = remove(input_image)
    return output_image

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    if not image_file.filename:
        return jsonify({'error': 'No selected image file'}), 400

    try:
        result_image = bgRemove(image_file)
        # Convert the PIL image to bytes data
        img_byte_array = BytesIO()
        result_image.save(img_byte_array, format='PNG')

        # Send the image bytes as the response with the appropriate content type
        return Response(img_byte_array.getvalue(), mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
