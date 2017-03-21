import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

from flask import Flask, jsonify
app = Flask(__name__)

import random
from preprocessing.data_prep import get_classes

IMAGE_DIR = '/Users/anjueappen/png'

@app.route("/prompts", methods=['GET'])
def prompts():
    return jsonify(get_classes(IMAGE_DIR))


@app.route("/submit", methods=['POST'])
def submit():
    return jsonify(dict([(cls, random.uniform(0.0, 1.0))
                           for cls in get_classes(IMAGE_DIR)]))


if __name__ == "__main__":
    app.run()