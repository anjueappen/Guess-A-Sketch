import sys, os
import tensorflow as tf
import logging
log = logging.getLogger(__name__)

sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))

from experiments.experiment import Experiment
from models.SketchCNN import SketchCNN # TODO use StarCNN
from preprocessing.data_prep import reload_K_splits

class Experiment4(Experiment):
    """
    Variables changed:
    - Train on a particular subset of labels, passed as a constructor parameter. The idea
      is to learn a specific category, e.g. animals, food, vehicles, ...
    - TODO Measure accuracy using a variant of the UI star-rating function, which is a log-softened
      function of two parameters:
        (1) the correct rank's label, when sorted descending by confidence, and
        (2) the correct rank's confidence, normalized like normalized = confidences/max(confidences)
    """
    _EXPERIMENT_ID = 4

    def __init__(self, log_dir=None, labels=None, name=None):
        """
        log_dir: an os.path for logs, optional
        """
        if not labels:
            raise ValueError('You have to pick some labels to train on. Theres no "all" default yet.')
        if not name:
            raise ValueError('You should give the experiment a name. If in doubt, use the name of the labels.')

        super(Experiment4, self).__init__(log_dir=log_dir)
        self.name = name

        # TensorFlow placeholders (memory allocations)
        self.image = tf.placeholder(tf.float32,
            [None, self._SKETCH_WIDTH, self._SKETCH_HEIGHT])
        self.label = tf.placeholder(tf.float32,
            [None, self._NUM_LABELS])
        self.keep_prob = tf.placeholder(tf.float32)

        self.model = SketchCNN(
            image=self.image,
            width=self._SKETCH_WIDTH,
            height=self._SKETCH_HEIGHT,
            num_labels=self._NUM_LABELS,
            label=self.label,
            keep_prob=0.5)

        self.train_set, self.test_set = reload_K_splits(
            self._INPUT_DIR,
            split_within_labels=True,
            labels=labels)

    def extra_info(self):
        return self.name

def main():
    standard = [
        'airplane', 'alarm clock', 'angel', 'ant', 'apple', 'arm', 'armchair', 'ashtray', 'axe', 'backpack', 'banana', 'barn', 'baseball bat',
        'basket', 'bathtub', 'bear (animal)', 'bed', 'bee', 'beer-mug', 'bell', 'bench', 'bicycle', 'binoculars', 'blimp', 'book', 'bookshelf',
        'boomerang', 'bottle opener', 'bowl', 'brain', 'bread', 'bridge', 'bulldozer', 'bus', 'bush', 'butterfly', 'cabinet', 'cactus', 'cake',
        'calculator', 'camel', 'camera', 'candle', 'cannon', 'canoe', 'car (sedan)', 'carrot', 'castle', 'cat', 'cell phone', 'chair', 'chandelier',
        'church', 'cigarette', 'cloud', 'comb', 'computer monitor', 'computer-mouse', 'couch', 'cow', 'crab', 'crane (machine)', 'crocodile',
        'crown', 'cup', 'diamond', 'dog', 'dolphin', 'donut', 'door', 'door handle', 'dragon', 'duck', 'ear', 'elephant', 'envelope', 'eye',
        'eyeglasses', 'face', 'fan', 'feather', 'fire hydrant', 'fish', 'flashlight', 'floor lamp', 'flower with stem', 'flying bird',
        'flying saucer', 'foot', 'fork', 'frog', 'frying-pan', 'giraffe', 'grapes', 'grenade', 'guitar', 'hamburger', 'hammer', 'hand', 'harp',
        'hat', 'head', 'head-phones', 'hedgehog', 'helicopter', 'helmet', 'horse', 'hot air balloon', 'hot-dog', 'hourglass', 'house', 'human-skeleton',
        'ice-cream-cone', 'ipod', 'kangaroo', 'key', 'keyboard', 'knife', 'ladder', 'laptop', 'leaf', 'lightbulb', 'lighter', 'lion', 'lobster',
        'loudspeaker', 'mailbox', 'megaphone', 'mermaid', 'microphone', 'microscope', 'monkey', 'moon', 'mosquito', 'motorbike', 'mouse (animal)',
        'mouth', 'mug', 'mushroom', 'nose', 'octopus', 'owl', 'palm tree', 'panda', 'paper clip', 'parachute', 'parking meter', 'parrot', 'pear', 'pen',
        'penguin', 'person sitting', 'person walking', 'piano', 'pickup truck', 'pig', 'pigeon', 'pineapple', 'pipe (for smoking)', 'pizza', 'potted plant',
        'power outlet', 'present', 'pretzel', 'pumpkin', 'purse', 'rabbit', 'race car', 'radio', 'rainbow', 'revolver', 'rifle', 'rollerblades', 'rooster',
        'sailboat', 'santa claus', 'satellite', 'satellite dish', 'saxophone', 'scissors', 'scorpion', 'screwdriver', 'sea turtle', 'seagull', 'shark',
        'sheep', 'ship', 'shoe', 'shovel', 'skateboard', 'skull', 'skyscraper', 'snail', 'snake', 'snowboard', 'snowman', 'socks', 'space shuttle',
        'speed-boat', 'spider', 'sponge bob', 'spoon', 'squirrel', 'standing bird', 'stapler', 'strawberry', 'streetlight', 'submarine', 'suitcase',
        'sun', 'suv', 'swan', 'sword', 'syringe', 't-shirt', 'table', 'tablelamp', 'teacup', 'teapot', 'teddy-bear', 'telephone', 'tennis-racket', 'tent',
        'tiger', 'tire', 'toilet', 'tomato', 'tooth', 'toothbrush', 'tractor', 'traffic light', 'train', 'tree', 'trombone', 'trousers', 'truck', 'trumpet',
        'tv', 'umbrella', 'van', 'vase', 'violin', 'walkie talkie', 'wheel', 'wheelbarrow', 'windmill', 'wine-bottle', 'wineglass', 'wrist-watch', 'zebra'
    ]
    food = [
        'apple', 'banana', 'bread', 'cake', 'carrot', 'donut', 'grapes', 'hamburger', 'mushroom',
        'pear', 'pineapple', 'pizza', 'pumpkin', 'strawberry', 'tomato'
    ]
    animals = [
        'ant', 'butterfly', 'camel', 'crab', 'crocodile', 'cat', 'cow', 'dog', 'dolphin',
        'dragon', 'duck', 'elephant', 'fish', 'flying bird', 'frog', 'giraffe', 'hedgehog',
        'horse', 'kangaroo', 'lion', 'lobster', 'monkey', 'mosquito', 'mouse (animal)',
        'octopus', 'owl', 'panda', 'parrot', 'penguin', 'pig', 'pigeon', 'rabbit', 'rooster',
        'scorpion', 'sea turtle', 'seagull', 'shark', 'sheep', 'snail', 'snake', 'spider',
        'squirrel', 'standing bird', 'tiger', 'zebra'
    ]
    easy = [
        'apple', 'axe', 'banana', 'baseball bat', 'book', 'candle', 'cloud', 'envelope', 'donut',
        'fork', 'key', 'spider'
    ]
    experiment = Experiment4(labels=standard, name='easy')
    # 1500 => 30 mins, 15000 => 5 hours
    few, lots = 1500, 15000
    experiment.run(iterations=few, save=True)

if __name__ == '__main__':
    main()
