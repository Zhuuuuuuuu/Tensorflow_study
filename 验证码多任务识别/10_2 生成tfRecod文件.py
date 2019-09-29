import tensorflow as tf
import os
import random
import math
import sys
from PIL import Image
import numpy as np

_NUM_TEST = 500

_RANDOM_SEED = 2

DATA_DIR = 'captcha/images/'

TFRECORD_DIR = 'captcha/'


def _tfdata_exists(dataset_dir):
    for split_name in ['train', 'test']:
        tf_name = os.path.join(dataset_dir, split_name + '.tfrecord')
        if not tf.gfile.Exists(tf_name):
            return False
    return True


def _get_filenames(dataset_dir):
    captcha_names = []
    for filename in os.listdir(dataset_dir):
        path = os.path.join(dataset_dir, filename)
        captcha_names.append(path)
    return captcha_names


def int64_feature(values):
    if not isinstance(values, (tuple, list)):
        values = [values]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=values))


def bytes_feature(values):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))


def image_to_tfexample(image_data, label0, label1, label2, label3):
    return tf.train.Example(features=tf.train.Features(feature={
        'image': bytes_feature(image_data),
        'label0': int64_feature(label0),
        'label1': int64_feature(label1),
        'label2': int64_feature(label2),
        'label3': int64_feature(label3)
    }))


# 数据转换为record格式
def _convert_dataset(split_name, filenames, tfrecord_dir):
    assert split_name in ['train', 'test']

    with tf.Session() as sess:
        out_tfnames = os.path.join(tfrecord_dir, split_name + '.tfrecord')
        with tf.python_io.TFRecordWriter(out_tfnames) as tf_writer:
            for i, filename in enumerate(filenames):
                try:
                    sys.stdout.write('\r>> Converting image %d/%d' % (i + 1, len(filenames)))
                    sys.stdout.flush()

                    image_data = Image.open(filename)
                    image_data = image_data.resize((224, 224))
                    image_data = image_data.convert('L').tobytes()

                    # 拿到4位验证码并encode()
                    labels = filename.split('/')[-1][:4]

                    example = image_to_tfexample(image_data, int(labels[0]), int(labels[1]), int(labels[2]),
                                                 int(labels[3]))
                    tf_writer.write(example.SerializeToString())

                except IOError as e:
                    print('Wrong: ' + filename)
                    print('Error: ', e)
                    print('Skip it\n')
    sys.stdout.write('\n')
    sys.stdout.flush()


if _tfdata_exists(TFRECORD_DIR):
    print('tf文件已存在')
else:
    photo_filenames = _get_filenames(DATA_DIR)

    random.seed(_RANDOM_SEED)
    # 打乱文件
    random.shuffle(photo_filenames)
    training_filenames = photo_filenames[_NUM_TEST:]
    testing_filenames = photo_filenames[:_NUM_TEST]

    _convert_dataset('train', training_filenames, TFRECORD_DIR)
    _convert_dataset('test', testing_filenames, TFRECORD_DIR)
    print('生成tfrecord文件')