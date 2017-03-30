import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from flask import Flask, jsonify, request
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
from io import BytesIO
import numpy as np

import scipy.misc
import base64

app = Flask(__name__)
CORS(app)

from preprocessing.data_prep import get_classes

IMAGE_DIR = 'png'
# print(os.path.join(os.path.dirname(__file__)))
META_FILE = 'SketchNet/experiments/2/mnist_basic.meta'


def eval_img(img):
    v = sess.run(output, feed_dict={image: img, keep_prob: 1.0})
    return v[0]

@app.route("/prompts", methods=['GET'])
def prompts():
    return jsonify(get_classes(IMAGE_DIR))

@app.route("/submit", methods=['POST'])
def submit():
    base64img = str(request.form['sketch']).split(',')[1]
    img = scipy.misc.imresize(np.array(Image.open(BytesIO(decode_base64(base64img)))), (225, 225))
    img = np.expand_dims(img, axis=0)

    result = eval_img(img)
    return jsonify([{
                        'label': cls,
                        'confidence': float(result[i])
                    } for i, cls in enumerate(get_classes(IMAGE_DIR))])


def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.decodestring(data)

if __name__ == "__main__":
    sess = tf.Session()
    new_saver = tf.train.import_meta_graph(META_FILE)
    new_saver.restore(sess, tf.train.latest_checkpoint('./experiments/2/'))

    inps = tf.get_collection('inputs')
    image = inps[0]
    keep_prob = inps[1]

    output = tf.get_collection('output')[0]
    app.run()


