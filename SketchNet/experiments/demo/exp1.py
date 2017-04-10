from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from utils import diy_slim
import tensorflow as tf

from preprocessing.data_prep import get_batch

FLAGS = None

LD = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(__file__).split('.')[0], 'tfboard')
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(__file__).split('.')[0], 'trained_model/')


def _mkdir_p(filepath):
    """ Makes all directories that filepath will be in, like mkdir -p
    Attribution: Krumelur
    Source: StackOverflow
    URL: http://stackoverflow.com/a/12517490
    Accessed: April 6, 2017
    """
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

_mkdir_p(SAVE_PATH)

def train():

    sess = tf.InteractiveSession()
    # Create a multilayer model.

    slim = tf.contrib.slim

    width = 225
    height = 225
    num_labels = 250
    batch_size = 135

    filter_1 = 64
    filter_2 = 128
    filter_3 = 256
    filter_4 = 512

    # Input placeholders
    with tf.name_scope('Input'):
        image = tf.placeholder(tf.float32, [None, width, height], name='input-img')
        label = tf.placeholder(tf.float32, [None, num_labels], name='ground-truth-label')
        keep_prob = tf.placeholder(tf.float32, name='keep-prob')

    with tf.name_scope('ReshapedInput'):
        x_image = tf.reshape(image, [-1, width, height, 1])

    with tf.name_scope('ConvPoolingLayer1'):
        h_conv1 = diy_slim.conv2d(x_image, filter_1, kernel_size=15, stride=3, padding='VALID')
        h_pool1 = diy_slim.max_pool2d(h_conv1, stride=2, kernel_size=3)

    with tf.name_scope('ConvPoolingLayer2'):
        h_conv2 = diy_slim.conv2d(h_pool1, filter_2, kernel_size=5, stride=1, padding='VALID')
        h_pool2 = diy_slim.max_pool2d(h_conv2, stride=2, kernel_size=3)

    with tf.name_scope('ConvPoolingLayer3'):
        h_conv3 = diy_slim.conv2d(h_pool2, filter_3, kernel_size=3, stride=1)
        h_conv4 = diy_slim.conv2d(h_conv3, filter_3, kernel_size=3, stride=1)
        h_conv5 = diy_slim.conv2d(h_conv4, filter_3, kernel_size=3, stride=1)
        h_pool5 = diy_slim.max_pool2d(h_conv5, stride=2, kernel_size=3, padding='VALID')

    with tf.name_scope('FlattenedConvOutput'):
        h_pool5_flat = tf.reshape(h_pool5, [-1, 7 * 7 * filter_3])

    with tf.name_scope('FCDropoutLayer1'):
        h_fc1 = diy_slim.fully_connected(h_pool5_flat, filter_4)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    with tf.name_scope('FCDropoutLayer2'):
        h_fc2 = diy_slim.fully_connected(h_fc1_drop, filter_4)
        h_fc2_drop = tf.nn.dropout(h_fc2, keep_prob)

    with tf.name_scope('FCPredictionLayer'):
        prediction = diy_slim.fully_connected(h_fc2_drop, num_labels)

    with tf.name_scope('CrossEntropyLoss'):
        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=label, logits=prediction))

    with tf.name_scope('TrainingStep'):
        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    with tf.name_scope('Accuracy'):
        with tf.name_scope('CorrectPrediction'):
            correct_prediction = tf.equal(tf.argmax(label, 1), tf.argmax(prediction, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    tf.summary.scalar('Accuracy vs Iterations', accuracy)
    tf.summary.scalar('Cross Entropy Loss vs Iterations', cross_entropy)
    tf.summary.image('Input Image', x_image, 9)

    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter(LD + '/train', sess.graph)
    test_writer = tf.summary.FileWriter(LD + '/test')
    tf.global_variables_initializer().run()


    def feed_dict(train):
        """Make a TensorFlow feed_dict: maps data onto Tensor placeholders."""
        if train:
            batch = get_batch(batch_size, (height, width))
            k = 0.5
        else:
            batch = get_batch(batch_size, (height, width), train=False)
            k = 1.0
        return {image: batch[0], label: batch[1], keep_prob: k}

    from tqdm import tqdm
    for i in tqdm(range(1)):
        if i % 10 == 0:  # Record summaries and test-set accuracy
            summary, acc = sess.run([merged, accuracy], feed_dict=feed_dict(False))
            test_writer.add_summary(summary, i)
            print('Accuracy at step %s: %s' % (i, acc))
        else:  # Record train set summaries, and train
            if i % 100 == 99:  # Record execution stats
                run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
                run_metadata = tf.RunMetadata()
                summary, _ = sess.run([merged, train_step],
                                      feed_dict=feed_dict(True),
                                      options=run_options,
                                      run_metadata=run_metadata)
                train_writer.add_run_metadata(run_metadata, 'step%03d' % i)
                train_writer.add_summary(summary, i)
                print('Adding run metadata for', i)
            else:  # Record a summary
                summary, _ = sess.run([merged, train_step], feed_dict=feed_dict(True))
                train_writer.add_summary(summary, i)

    tf.add_to_collection('inputs', image)
    tf.add_to_collection('inputs', keep_prob)
    tf.add_to_collection('output', prediction)
    # tf.add_to_collection('embedding', self.model.img_embedding)
    saver = tf.train.Saver()
    saver.save(sess, SAVE_PATH)
    print("TensorBoard Output: {}".format(LD))
    print("Trained Model Output: {}".format(SAVE_PATH))



    train_writer.close()
    test_writer.close()


train()
