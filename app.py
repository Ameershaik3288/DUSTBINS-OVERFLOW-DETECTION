from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import numpy as np
from keras.preprocessing import image
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
model = tf.keras.models.load_model('dustbin_overflow_cnn.h5')

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CLASS_NAMES = ['normal', 'overflow']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(image_path)

            img = image.load_img(image_path, target_size=(128, 128))
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            preds = model.predict(img_array)
            prediction = CLASS_NAMES[np.argmax(preds)]
            confidence = round(np.max(preds) * 100, 2)
            detected_datetime = datetime.now()
            detected_date = detected_datetime.strftime('%d-%m-%Y')
            detected_time = detected_datetime.strftime('%I:%M:%S %p')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            detected_location = request.remote_addr or 'Not Available'

            try:
                if latitude and longitude:
                    lat_value = float(latitude)
                    lon_value = float(longitude)
                    detected_location = f'Latitude: {lat_value:.6f}, Longitude: {lon_value:.6f}'
            except ValueError:
                pass

            officer_message = 'OVERFLOW DETECTED! LOCATION AND TIME IS SENT TO MUNICIPAL OFFICERS AND LOCAL AREA SANITIZATION WORKERS.'

            return redirect(url_for(
                'result',
                prediction=prediction,
                confidence=confidence,
                image_filename=unique_filename,
                detected_at=f'{detected_date} {detected_time}',
                detected_date=detected_date,
                detected_time=detected_time,
                detected_location=detected_location,
                officer_message=officer_message
            ))

        return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/result')
def result():
    prediction = request.args.get('prediction')
    confidence = request.args.get('confidence')
    image_filename = request.args.get('image_filename')
    detected_at = request.args.get('detected_at')
    detected_date = request.args.get('detected_date')
    detected_time = request.args.get('detected_time')
    detected_location = request.args.get('detected_location', 'Not Available')
    officer_message = request.args.get(
        'officer_message',
        'OVERFLOW DETECTED! LOCATION AND TIME IS SENT TO MUNICIPAL OFFICERS AND LOCAL AREA SANITIZATION WORKERS.'
    )

    if not prediction or confidence is None or not image_filename:
        return redirect(url_for('index'))

    image_url = url_for('static', filename=f'uploads/{image_filename}')

    return render_template(
        'result.html',
        prediction=prediction,
        confidence=confidence,
        image_url=image_url,
        detected_at=detected_at,
        detected_date=detected_date,
        detected_time=detected_time,
        detected_location=detected_location,
        officer_message=officer_message
    )

if __name__ == '__main__':
    app.run(debug=True)
