import sys, os
import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))

from utils.tf_graph_scope import define_scope
from preprocessing.tf_data_prep import populate_batch, preprocess
from utils.base_model import Model
from utils.tf_utils import weight_variable, bias_variable, conv2d, max_pool_2x2


class Exp1Model(Model):

    @define_scope
    def prediction(self):
        filter_1 = 32
        filter_2 = 64
        filter_3 = 1024

        # Layer 1
        W_conv1 = weight_variable([5, 5, 1, filter_1])
        b_conv1 = bias_variable([filter_1])

        x_image = tf.reshape(self.image, [-1, self.width, self.height, 1])  # TODO: probably removable

        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
        h_pool1 = max_pool_2x2(h_conv1)

        # Layer 2

        W_conv2 = weight_variable([5, 5, filter_1, filter_2])
        b_conv2 = bias_variable([filter_2])

        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = max_pool_2x2(h_conv2)

        # Layer 3 - Densely Connected

        W_fc1 = weight_variable([125 * 125 * filter_2, filter_3])
        b_fc1 = bias_variable([filter_3])

        h_pool2_flat = tf.reshape(h_pool2, [-1, 125 * 125 * filter_2])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

        # Dropout Layer

        h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)

        # Readout Layer - classify the images
        W_fc2 = weight_variable([filter_3, self.num_labels])
        b_fc2 = bias_variable([self.num_labels])

        y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
        return y_conv

    @define_scope
    def train(self):
        cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=self.label, logits=self.prediction))
        return tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    @define_scope
    def accuracy(self):
        correct_prediction = tf.equal(tf.argmax(self.label, 1), tf.argmax(self.prediction, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return accuracy


def main():
    # TODO Hard Coding!!!
    train = True
    width = 500
    height = 500
    num_labels = 250

    image = tf.placeholder(tf.float32, [None, width, height, 1])
    label = tf.placeholder(tf.float32, [None, num_labels])
    keep_prob = tf.placeholder(tf.float32)

    model = Exp1Model(image, width, height, num_labels, label, keep_prob)

    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        ground_truth_mapping = preprocess('/Users/anjueappen/png')

        for i in range(1000):
            print(i)
            batch = populate_batch(ground_truth_mapping[:50], (height, width))
            sess.run(model.train, {image: batch[0], label: batch[1], keep_prob: 0.5})

            if i % 100 == 0:
                train_accuracy = sess.run(model.accuracy, {image: batch[0], label: batch[1], keep_prob: 1.0})
                print("step %d, training accuracy %g" % (i, train_accuracy))

            import random;
            random.shuffle(ground_truth_mapping)

        batch = populate_batch(ground_truth_mapping[:50], (height, width))
        acc = sess.run(model.accuracy, {image: batch[0], label: batch[1], keep_prob: 1.0})
        print("test accuracy %g" % acc)


if __name__ == '__main__':
    main()
