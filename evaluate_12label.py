#! /usr/bin/python
# -*- coding: utf-8 -*-
''' AdapNet++:  Self-Supervised Model Adaptation for Multimodal Semantic Segmentation

 Copyright (C) 2018  Abhinav Valada, Rohit Mohan and Wolfram Burgard

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.'''

import argparse
import datetime
import importlib
import os
import cv2
import numpy as np
import tensorflow as tf
import yaml
import time
from dataset.helper import *
import matplotlib.pyplot as plt
from PIL import Image

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-c', '--config', default='config/cityscapes_test.config')
PARSER.add_argument('-d', '--save_directory', default='None', help='seve_directory')
args = PARSER.parse_args()

def test_func(config):
    os.environ['CUDA_VISIBLE_DEVICES'] = config['gpu_id']
    module = importlib.import_module('models.' + config['model'])
    model_func = getattr(module, config['model'])
    data_list, iterator = get_test_data(config)
    resnet_name = 'resnet_v2_50'

    with tf.variable_scope(resnet_name):
        model = model_func(num_classes=config['num_classes'], training=False)
        images_pl = tf.placeholder(tf.float32, [None, config['height'], config['width'], 3])
        model.build_graph(images_pl)

    config1 = tf.ConfigProto()
    config1.gpu_options.allow_growth = True
    sess = tf.Session(config=config1)
    sess.run(tf.global_variables_initializer())
    import_variables = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
    print 'total_variables_loaded:', len(import_variables)
    saver = tf.train.Saver(import_variables)
    saver.restore(sess, config['checkpoint'])
    sess.run(iterator.initializer)
    step = 0
    total_num = 0
    output_matrix = np.zeros((config['num_classes'], 3))
    print("class: "),
    print(config['num_classes'])
    
    i = 0

    while 1:
        try:
            img, label = sess.run([data_list[0], data_list[1]])
            feed_dict = {images_pl : img}
            probabilities = sess.run([model.softmax], feed_dict=feed_dict)
            prediction = np.argmax(probabilities[0], 3)
            gt = np.argmax(label, 3)

            #####void(0)を表示させるとき
            prediction[gt == 0] = 0
            #####

            segmented_image = np.zeros_like(img)
            # BGR
            segmented_image[prediction ==  0] = [  0,  0,  0]
            segmented_image[prediction ==  1] = [ 180,130,70]
            segmented_image[prediction ==  2] = [ 70, 70, 70]
            segmented_image[prediction ==  3] = [128, 64,128]
            segmented_image[prediction ==  4] = [232, 35,244]
            segmented_image[prediction ==  5] = [153,153,190]
            segmented_image[prediction ==  6] = [ 35,142,107]
            segmented_image[prediction ==  7] = [153,153,153]
            segmented_image[prediction ==  8] = [142,  0,  0]
            segmented_image[prediction ==  9] = [  0,220,220]
            segmented_image[prediction == 10] = [ 60, 20,220]
            segmented_image[prediction == 11] = [ 32, 11,119]
            
   
            segmented_image1=segmented_image.reshape([config['height'], config['width'], 3])
            
            ######表示######
            #表示のため正規化
            #segmented_image2 = np.array(segmented_image1)
            #segmented_image2 = segmented_image2/255
            #cv2.imshow('image',segmented_image2)
            #cv2.waitKey(1)
            ######
            
            if args.save_directory != 'None':
                print("save_place:"),
                print(args.save_directory)
                print("\n")
                cv2.imwrite(args.save_directory + str(i) +'.png',segmented_image1)
            i = i + 1
            
            
            output_matrix = compute_output_matrix(gt, prediction, output_matrix)
            
            total_num += label.shape[0]
            if (step+1) % config['skip_step'] == 0:
                print '%s %s] %d. iou updating' \
                  % (str(datetime.datetime.now()), str(os.getpid()), total_num)
                print 'mIoU: ', compute_iou(output_matrix)

                print('Sky:                         '),
                print(  output_matrix[1, 0]/(np.sum(output_matrix[1,0:])+1e-10)*100  )

                print('Building:                    '),
                print(  output_matrix[2, 0]/(np.sum(output_matrix[2,0:])+1e-10)*100  )
                
                print('Road:                        '),
                print(  output_matrix[3, 0]/(np.sum(output_matrix[3,0:])+1e-10)*100  )

                print('SideWalk:                    '),
                print(  output_matrix[4, 0]/(np.sum(output_matrix[4,0:])+1e-10)*100  )
                
                print('Fence:                       '),
                print(  output_matrix[5, 0]/(np.sum(output_matrix[5,0:])+1e-10)*100  )
                
                print('Vegetation:                  '),
                print(  output_matrix[6, 0]/(np.sum(output_matrix[6,0:])+1e-10)*100  )
                
                print('Pole:                        '),
                print(  output_matrix[7, 0]/(np.sum(output_matrix[7,0:])+1e-10)*100  )
                
                print('Car/Truck/Bus:               '),
                print(  output_matrix[8, 0]/(np.sum(output_matrix[8,0:])+1e-10)*100  )
                
                print('Traffic Sign:                '),
                print(  output_matrix[9, 0]/(np.sum(output_matrix[9,0:])+1e-10)*100  )
                
                print('Pedestrians:                 '),
                print(  output_matrix[10, 0]/(np.sum(output_matrix[10,0:])+1e-10)*100  )
                
                print('Rider/Bicycle/Motorcycle:    '),
                print(  output_matrix[11, 0]/(np.sum(output_matrix[11,0:])+1e-10)*100  )

            step += 1


        except tf.errors.OutOfRangeError:
            print 'mIoU: ', compute_iou(output_matrix), ' total_data: ', total_num
            break

def main():
    args = PARSER.parse_args()
    if args.config:
        file_address = open(args.config)
        config = yaml.load(file_address)
    else:
        print '--config config_file_address missing'
    test_func(config)

if __name__ == '__main__':
    main()
