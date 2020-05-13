#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import argparse
import numpy as np
import os

h = 375
w = 1275

HEIGHT = 384
WIDTH = 768

# ラベル画像を色からラベル番号に変更する関数
def change_label(src):

    # 出力画像用の配列生成（要素は全て空）
    dst = np.empty((h,w))
    dst_color = np.empty((h,w,3))
    i=0
    # このループ死ぬほど遅いと思う　C++やCython使ったり、書き方工夫すれば早くなります。
    # 簡易的に作ったのですいません
    #↓carlaのラベル対応表
    # https://github.com/carla-simulator/carla/blob/master/LibCarla/source/carla/image/CityScapesPalette.h
    # adapnetppで一般の12classに変換(sky例外 riderがないため実質11class) 参考：onedrive label12.png
    for img_line in src:
        j = 0
        for img_px in img_line:
            #opencvではBGR
            if (img_px == [  0,  0,  0]).all():#unlabeled→void
                dst[i,j] = 0
                dst_color[i,j] = [  0,  0,  0]
            elif (img_px == [ 70, 70, 70]).all():#building
                dst[i,j] = 2
                dst_color[i,j] = [ 70, 70, 70]
            elif (img_px == [153,153,190]).all():#fence
                dst[i,j] = 5
                dst_color[i,j] = [153,153,190]
            elif (img_px == [160,170,250]).all():#other→void
                dst[i,j] = 0
                dst_color[i,j] = [  0,  0,  0]
            elif (img_px == [ 60, 20,220]).all():#pedestrian
                dst[i,j] = 10
                dst_color[i,j] = [ 60, 20,220]
            elif (img_px == [153,153,153]).all():#pole
                dst[i,j] = 7
                dst_color[i,j] = [153,153,153]
            elif (img_px == [ 50,234,157]).all():#road line→sky skyがなかったのでroad lineは有効にした
                dst[i,j] = 1
                dst_color[i,j] = [180,130, 70]
            elif (img_px == [128, 64,128]).all():#road
                dst[i,j] = 3
                dst_color[i,j] = [128, 64,128]
            elif (img_px == [232, 35,244]).all():#sidewalk
                dst[i,j] = 4
                dst_color[i,j] = [232, 35,244]
            elif (img_px == [ 35,142,107]).all():#vegetation
                dst[i,j] = 6
                dst_color[i,j] = [ 35,142,107]
            elif (img_px == [142,  0,  0]).all():#car
                dst[i,j] = 8
                dst_color[i,j] = [142,  0,  0]
            elif (img_px == [156,102,102]).all():#wall→Fence
                dst[i,j] = 5
                dst_color[i,j] = [153,153,190]
            elif (img_px == [  0,220,220]).all():#traffic sign
                dst[i,j] = 9
                dst_color[i,j] = [  0,220,220]
            j = j + 1
        i = i + 1

        #変更後 
        #unlabeledとotherで分けられているのが、わかりにくいため統合した
        #それに伴いskyが無かったためroad lineに入れ替えた
        #0:void
        #1:road line
        #2:building
        #3:road
        #4:sidewalk
        #5:fence
        #6:vegetation
        #7:pole
        #8:car
        #9:traffic sign
        #10pedestrians
        #好きなようにラベルを変えて大丈夫です。
    return dst, dst_color


def main():

    #RGB画像の処理
    print("#####RGB#####")
    read_path1 = parser.input_rgb
    file_list1 = os.listdir(read_path1)
    for file_name in file_list1:
        # basename: all filename in read_path
        basename = os.path.basename(file_name)
        print(basename)
        
        # name back match
        if basename.endswith('.png'):
            abs_name = read_path1 + file_name
            rgb_img = cv2.imread(abs_name)
            
            # バイリニア補間でリサイズ
            rgb_img_resize = cv2.resize(rgb_img, (WIDTH, HEIGHT))
            cv2.imwrite(parser.output_rgb + "rgb_" + file_name, rgb_img_resize)


    #ラベル画像の処理
    print("#####label#####")
    read_path2 = parser.input_label
    file_list2 = os.listdir(read_path2)
    for file_name in file_list2:
        # basename: all filename in read_path
        basename = os.path.basename(file_name)
        print(basename)
        
        # name back match
        if basename.endswith('.png'):
            abs_name = read_path2 + file_name
            color_label_img = cv2.imread(abs_name)
            # カラーからラベルへ 変更したカラー画像も生成
            label_img,label_img_change_color = change_label(color_label_img)
            
            # 最近傍補間でリサイズ
            label_img_resize = cv2.resize(label_img, (WIDTH, HEIGHT),interpolation=cv2.INTER_NEAREST)
            # バイリニア補間でリサイズ
            label_img_change_color_resize = cv2.resize(label_img_change_color, (WIDTH, HEIGHT))
            cv2.imwrite(parser.output_label + "label_" + file_name, label_img_resize)
            cv2.imwrite(parser.output_color_label + "label_color_" + file_name, label_img_change_color_resize)

    


def get_parser():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-i', '--input_rgb', help='rgb_input_image_dir')
    parser.add_argument('-j', '--input_label', help='label_input_image_dir')
    parser.add_argument('-o', '--output_rgb', help='rgb_output_image_dir')
    parser.add_argument('-p', '--output_label', help='label_output_image_dir')
    parser.add_argument('-q', '--output_color_label', help='changed_color_label_output_image_dir')

    # 例　python resize_and_change_label_images.py -i ./rgb_img/ -j ./label_img/ -o ./output/rgb_img/ -p ./output/label_img/ -q ./output/color_label_img/
    return parser


if __name__ == '__main__':
    parser = get_parser().parse_args()
    main()