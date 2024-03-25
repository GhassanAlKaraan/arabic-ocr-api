import os
from flask import Flask, request, jsonify
from ArabicOcr import arabicocr

app = Flask(__name__)


# Request: POST http://127.0.0.1:5000/scan
# Body: file
# Header: apikey = ghass.dev
@app.route("/scan", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "text": "File attached is invalid"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "text": "No selected file"})

    if file and allowed_file(file.filename):
        # Check if the user is authenticated
        if not authenticate(request):
            return jsonify({"success": False, "text": "Invalid apikey"})
        # Do OCR here
        result = extract_text(file)
        if result is None:
            return jsonify({"success": False, "text": "OCR failed"})
        return jsonify({"success": True, "text": result})
    else:
        return jsonify({"success": False, "text": "File format not supported"})


def extract_text(file):
    # Save the uploaded image
    image_path = os.path.join("uploads", file.filename)
    file.save(image_path)
    out_image = os.path.join("scans", file.filename)
    text_file = os.path.join("results", file.filename + '.txt')

    # Perform OCR here
    results = arabicocr.arabic_ocr(image_path, out_image)

    words = []
    for i in range(len(results)):
        word = results[i][1]
        words.append(word)
    with open(text_file, 'w', encoding='utf-8') as myfile:
        myfile.write(str(words))

    # Remove the uploaded image
    os.remove(image_path)

    return words


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

def authenticate(req):
    secret_key = 'ghass.dev'

    if 'apikey' not in req.headers:
        return False
    apikey = req.headers['apikey']
    if apikey != secret_key:
        return False
    return True


def main():
    app.run(port=int(os.environ.get('PORT', 9000)))


if __name__ == "__app__":
    main()
