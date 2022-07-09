#!/usr/bin/env python3
"""! @brief This python file allows to train the BeeModel"""
##
# @file train_network.py
#
# @brief This file is used to train the BeeModel which is used
#        in the BeeAlarmed project
#
# @section authors Author(s)
# - Created by Fabian Hickert, 2021
#

import argparse
import tensorflow as tf
import tensorflow_datasets as tfds
import BeeModel

print("=" * 30)
try:
    from BeeDataset.bee_dataset import BeeDataset

    print("Using local Bee-Dataset")
except:
    print("Using Bee-Dataset from TFDS installation")
print("=" * 30)

# Allow growth
# pylint: disable=no-member
# config = tf.compat.v1.ConfigProto()
# config.gpu_options.allow_growth = True
# session = tf.compat.v1.InteractiveSession(config=config)

parser = argparse.ArgumentParser()
parser.add_argument("--gpu", action="store_true",
                    help="Use --gpu=True to train network with GPU and nothing to train on CPU.")
args = parser.parse_args()

# Jetson Nano GPU
if args.gpu:
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.75  # limit memory allocation to avoid killing the process
    config.gpu_options.allow_growth = True
    session = tf.compat.v1.InteractiveSession(config=config)

MODEL_SAVE_PATH = "SavedModel"

# Load via TFDS
train, val = tfds.load('bee_dataset/bee_dataset_150',
                       batch_size=11,  # 100, #changed batch to load to Jetson Nano to avoid process kill
                       as_supervised=True,
                       split=["train[0%:50%]", "train[50%:100%]"])

if args.gpu:
    # Use GPU to train network
    with tf.device('/GPU:0'):
        # Get the BeeModel and train it
        model = BeeModel.get_bee_model(150, 75)
        model.fit(
            train,
            validation_data=val,
            epochs=20,
            verbose=1,
            callbacks=[]
        )
else:
    model = BeeModel.get_bee_model(150, 75)
    model.fit(
        train,
        validation_data=val,
        epochs=20,
        verbose=1,
        callbacks=[]
    )

# Save the model and show the summary
model.save(MODEL_SAVE_PATH)
model.summary()
