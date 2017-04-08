import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import labels
import hashlib
from flask import Flask, jsonify, request
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
from io import BytesIO
import numpy as np
import scipy.misc
import base64
from err import ClassificationFailure
from preprocessing.data_prep import get_classes

app = Flask(__name__)
CORS(app)

# ###
# Constants, don't change these
# ###
__PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
__IMAGE_DIR = os.path.join(__PROJECT_ROOT, 'png')
# Keep in sync with experiments.experiment.Experiment, TODO refactor
__TRAINED_MODEL_DIR = os.path.join(__PROJECT_ROOT, 'SketchNet', 'trained_models')

# ###
# Choose which trained model to use.
# - MODEL is the directory in trained_models. Usually indicates experiment number & dataset.
# - META is which meta file (-> graph definition) to use inside that folder
#   - version filenames look like "timestamp_experiment-name_model-name_trained_iterations"
# - LABELS should be the same as the model was trained on, see labels.py
#
# The API will serve the model with
# - the latest .index/.data training information, specified by the checkpoint file in MODEL
# - the .meta graph definition, specified by MODEL
# - the ordered list of labels they were trained on, specified by LABELS
#
# Warnings
# - If the checkpoint, meta, index, or data files don't exist, it'll crash on startup.
# - If the model is incompatible with the current API, it might run, then break on POST /submit.
# ###
MODEL = 'exp5easy'
META = '20170407-220659_exp5easy_SketchCNN-trained-1500.meta'
LABELS = labels.easy
# Use the input, build full paths.
__CHECKPOINT_DIR = os.path.join(__TRAINED_MODEL_DIR, MODEL)
__META_FILE = os.path.join(__CHECKPOINT_DIR, META)


def eval_img(img):
    import pdb; pdb.set_trace()
    v = sess.run(prediction_tensor, {
        image_tensor: img,
        keep_prob_tensor: 1.0
    })
    return v[0]

@app.route("/prompts", methods=['GET'])
def prompts():
    return jsonify(get_classes(__IMAGE_DIR))

@app.route("/submit", methods=['POST'])
def submit():
    try:
        base64img = str(request.form['sketch']).split(',')[1]
        img = scipy.misc.imresize(np.array(Image.open(BytesIO(decode_base64(base64img)))), (225, 225))

        # handle color channels
        if len(img.shape) > 2:
            img = img[:, :, 0] + img[:, :, 1] + img[:, :, 2]
            img[img > 0] = 255

        # add batch_size dimension
        img = np.expand_dims(img, axis=0)

        result = eval_img(img)
        # TODO normalize (or not)
        # result = result / max(result)
        return jsonify([{
                            'label': label,
                            'confidence': float(result[i])
                        } for i, label in enumerate(LABELS)])
    except Exception as e:
        raise ClassificationFailure(message=str(e))


@app.errorhandler(ClassificationFailure)
def handle_classification_failure(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

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
    try:
        new_saver = tf.train.import_meta_graph(__META_FILE)
        new_saver.restore(sess, tf.train.latest_checkpoint(__CHECKPOINT_DIR))

        inps = tf.get_collection('inputs')
        image_tensor = inps[0]
        keep_prob_tensor = inps[1]
        # Legacy experiment support.
        # The keep_prob Tensor should have shape None, cause it's a scalar.
        # However, once upon a time, inps[1] was the labels Tensor with shape (None,250), instead of
        # the keep_prob Tensor with shape None, because Ross is a donut.
        # This is a cheesy fix which makes the API work even with trained models from that dark era.
        # The end.
        if keep_prob_tensor.shape is not None and len(inps) > 2:
            keep_prob_tensor = inps[2]

        prediction_tensor = tf.get_collection('output')[0]
    except Exception as e:
        print(e)
        raise
    app.run()
