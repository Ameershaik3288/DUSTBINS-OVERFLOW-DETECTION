from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from keras.preprocessing import image
import os

app = Flask(__name__)
model = tf.keras.models.load_model('dustbin_overflow_cnn.h5')

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CLASS_NAMES = ['normal', 'overflow']

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
    image_path = None

    if request.method == 'POST':
        file = request.files['file']
        if file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)

            img = image.load_img(image_path, target_size=(128, 128))
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            preds = model.predict(img_array)
            prediction = CLASS_NAMES[np.argmax(preds)]
            confidence = round(np.max(preds) * 100, 2)

    return render_template('index.html',
                           prediction=prediction,
                           confidence=confidence,
                           image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True)
