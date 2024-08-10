from flask import Flask, render_template, request, send_file, redirect, url_for
import qrcode
import pyotp
import uuid
import os

app = Flask(__name__)
data_store = {}


@app.route('/')
def index():
    return render_template('manudash.html')


@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    batch_number = request.form['batch_number']
    expiry_date = request.form['expiry_date']
    barcode = request.form['barcode']

    unique_id = str(uuid.uuid4())
    data_store[unique_id] = {
        'name': name,
        'batch_number': batch_number,
        'expiry_date': expiry_date,
        'barcode': barcode,
        'verified': False
    }
    verification_url = f'http://127.0.0.1:5000/verify/{unique_id}'
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(verification_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image
    filename = f'static/qr_code_{unique_id}.png'
    img.save(filename)

    # Provide an option to download the QR code image
    return render_template('manudash.html', qr_image=filename,
                           qr_download_url=url_for('download_qr', filename=filename))


@app.route('/download_qr/<path:filename>', methods=['GET'])
def download_qr(filename):
    return send_file(filename, as_attachment=True)


@app.route('/verify/<unique_id>', methods=['GET', 'POST'])
def verify(unique_id):
    if request.method == 'POST':
        password_input = request.form['password']

        if unique_id in data_store:
            data = data_store[unique_id]
            if password_input == data['otp']:
                # Remove the OTP and mark the data as verified
                data_store.pop(unique_id)
                return render_template('success.html', name=data['name'],
                                       batch_number=data['batch_number'],
                                       expiry_date=data['expiry_date'],
                                       barcode=data['barcode'])
            else:
                return "Invalid password! Please try again."
        else:
            return "No data found or QR code already verified!"

    else:
        if unique_id in data_store and not data_store[unique_id]['verified']:
            otp = pyotp.random_base32()
            data_store[unique_id]['otp'] = otp
            data_store[unique_id]['verified'] = True

            # Print OTP to terminal
            print(f'Generated OTP for {unique_id}: {otp}')

            return render_template('verify.html', unique_id=unique_id, otp=otp)
        else:
            return "Invalid or already verified QR code!"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
