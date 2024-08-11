from flask import Flask, render_template, request, redirect, url_for, jsonify
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def read_qr_code_from_image(image_path):
    """Reads a QR code from the image at the given path."""
    img = cv2.imread(image_path)
    qr_codes = decode(img)
    for qr_code in qr_codes:
        return qr_code.data.decode("utf-8")
    return None


def is_url(data):
    """Checks if the given data is a URL."""
    url_regex = re.compile(r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$', re.IGNORECASE)
    return re.match(url_regex, data) is not None


@app.route('/')
def index():
    """Renders the main page."""
    return render_template('pharma.html')


@app.route('/upload', methods=['POST'])
def upload():
    """Handles the upload of a QR code image."""
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        qr_data = read_qr_code_from_image(file_path)

        if qr_data:
            if is_url(qr_data):
                return redirect(qr_data)
            else:
                return f"QR code data: {qr_data}"
        else:
            return "No QR code detected!"


@app.route('/scan', methods=['POST'])
def scan():
    """Handles real-time scanning of a QR code using the webcam."""
    cap = cv2.VideoCapture(0)
    qr_data = None

    while True:
        ret, frame = cap.read()
        qr_codes = decode(frame)

        for qr_code in qr_codes:
            qr_data = qr_code.data.decode("utf-8")
            break

        if qr_data:
            break

        cv2.imshow('Scanning QR Code...', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if qr_data:
        if is_url(qr_data):
            return redirect(qr_data)
        else:
            return jsonify({"qr_data": qr_data})
    else:
        return "No QR code detected!"


@app.route('/submit_barcode', methods=['POST'])
def submit_barcode():
    """Handles the submission of a barcode."""
    barcode = request.form.get('barcode')
    # Implement logic to verify barcode from a database or other sources
    # Assuming we return a mock response for now
    if barcode:
        # Replace this with actual verification logic
        return jsonify({"status": "success", "barcode_data": barcode})
    else:
        return jsonify({"status": "failed", "message": "Invalid barcode"})


@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    """Handles the verification of an OTP."""
    unique_id = request.form.get('unique_id')
    # Implement your logic for verifying OTP
    # For now, return a mock response
    return jsonify({"status": "success", "unique_id": unique_id})


@app.route('/history')
def history():
    """Displays the scan history (mock implementation)."""
    # You can replace this with actual logic to display scan history
    return "This is the scan history page."


if __name__ == '__main__':
    app.run(debug=True, port=5001)
