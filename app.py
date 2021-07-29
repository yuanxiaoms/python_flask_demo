from flask import Flask, render_template, request
from werkzeug import secure_filename
from tensorflow import keras
import tensorflow as tf

app = Flask(__name__)

@app.route("/")
def index():    
    return render_template("index.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
    
      image_size = (180, 180)
      img = keras.preprocessing.image.load_img("PetImages/Cat/6779.jpg", target_size=image_size)
      img_array = keras.preprocessing.image.img_to_array(img)
      img_array = tf.expand_dims(img_array, 0)  # Create batch axis

      model = keras.models.load_model('cat_dog')
      predictions = model.predict(img_array)
      score = predictions[0]
      ret = "This image is %.2f percent cat and %.2f percent dog." % (100 * (1 - score), 100 * score))
      return 'file uploaded successfully ' + ret

if __name__ == '__main__':
    app.run(debug=True)
        
