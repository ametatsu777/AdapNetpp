#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import argparse
import numpy as np
import os
import time
import datetime


HEIGHT = 384
WIDTH = 768

# ラベル画像を色からラベル番号に変更する関数
def change_label(src):

    # 出力画像用の配列生成（要素は全て空）
    h, w = src.shape[:2]
    dst = np.empty((h,w))
    dst_color = np.empty((h,w,3))
    i=0
    #↓carlaのラベル対応表
    # https://github.com/carla-simulator/carla/blob/master/LibCarla/source/carla/image/CityScapesPalette.h
    # adapnetppで一般の12classに変換(sky例外 riderがないため実質11class) 参考：onedrive label12.png

    lbl_0 = np.where((src[ :, :, 0] == 0) & (src[ :, :, 1] == 0) & (src[ :, :, 2] == 0))
    lbl_1 = np.where((src[ :, :, 0] == 70) & (src[ :, :, 1] == 70) & (src[ :, :, 2] == 70))
    lbl_2 = np.where((src[ :, :, 0] == 153) & (src[ :, :, 1] == 153) & (src[ :, :, 2] == 190))
    lbl_3 = np.where((src[ :, :, 0] == 160) & (src[ :, :, 1] == 170) & (src[ :, :, 2] == 250))
    lbl_4 = np.where((src[ :, :, 0] == 60) & (src[ :, :, 1] == 20) & (src[ :, :, 2] == 220))
    lbl_5 = np.where((src[ :, :, 0] == 153) & (src[ :, :, 1] == 153) & (src[ :, :, 2] == 153))
    lbl_6 = np.where((src[ :, :, 0] == 50) & (src[ :, :, 1] == 234) & (src[ :, :, 2] == 157))
    lbl_7 = np.where((src[ :, :, 0] == 128) & (src[ :, :, 1] == 64) & (src[ :, :, 2] == 128))
    lbl_8 = np.where((src[ :, :, 0] == 232) & (src[ :, :, 1] == 35) & (src[ :, :, 2] == 244))
    lbl_9 = np.where((src[ :, :, 0] == 35) & (src[ :, :, 1] == 142) & (src[ :, :, 2] == 107))
    lbl_10 = np.where((src[ :, :, 0] == 142) & (src[ :, :, 1] == 0) & (src[ :, :, 2] == 0))
    lbl_11 = np.where((src[ :, :, 0] == 156) & (src[ :, :, 1] == 102) & (src[ :, :, 2] == 102))
    lbl_12 = np.where((src[ :, :, 0] == 0) & (src[ :, :, 1] == 220) & (src[ :, :, 2] == 220))
    
    dst_color[lbl_0[0], lbl_0[1]] = [  0,  0,  0]
    dst_color[lbl_1[0], lbl_1[1]] = [ 70, 70, 70]
    dst_color[lbl_2[0], lbl_2[1]] = [153,153,190]
    dst_color[lbl_3[0], lbl_3[1]] = [  0,  0,  0]
    dst_color[lbl_4[0], lbl_4[1]] = [ 60, 20,220]
    dst_color[lbl_5[0], lbl_5[1]] = [153,153,153]
    dst_color[lbl_6[0], lbl_6[1]] = [180,130, 70]
    dst_color[lbl_7[0], lbl_7[1]] = [128, 64,128]
    dst_color[lbl_8[0], lbl_8[1]] = [232, 35,244]
    dst_color[lbl_9[0], lbl_9[1]] = [ 35,142,107]
    dst_color[lbl_10[0], lbl_10[1]] = [142,  0,  0]
    dst_color[lbl_11[0], lbl_11[1]] = [153,153,190]
    dst_color[lbl_12[0], lbl_12[1]] = [  0,220,220]
    
    dst[lbl_0[0], lbl_0[1]] = 0
    dst[lbl_1[0], lbl_1[1]] = 2
    dst[lbl_2[0], lbl_2[1]] = 5
    dst[lbl_3[0], lbl_3[1]] = 0
    dst[lbl_4[0], lbl_4[1]] = 10
    dst[lbl_5[0], lbl_5[1]] = 7
    dst[lbl_6[0], lbl_6[1]] = 1
    dst[lbl_7[0], lbl_7[1]] = 3
    dst[lbl_8[0], lbl_8[1]] = 4
    dst[lbl_9[0], lbl_9[1]] = 6
    dst[lbl_10[0], lbl_10[1]] = 8
    dst[lbl_11[0], lbl_11[1]] = 5
    dst[lbl_12[0], lbl_12[1]] = 9
    
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
    count_rgb = 0.0
    count_rgb_int = 0
    for file_name in file_list1:
        # basename: all filename in read_path
        basename = os.path.basename(file_name)
        print(basename)        
        # name back match
        if basename.endswith('.png') or basename.endswith('.jpg') or basename.endswith('.jpeg'):
            abs_name = read_path1 + file_name
            rgb_img = cv2.imread(abs_name)           
            # バイリニア補間でリサイズ
            rgb_img_resize = cv2.resize(rgb_img, (WIDTH, HEIGHT))
            cv2.imwrite(parser.output_rgb + "rgb_" + file_name, rgb_img_resize)
            count_rgb = count_rgb + 1
            count_rgb_int = count_rgb_int + 1

    #ラベル画像の処理
    print("#####label#####")
    read_path2 = parser.input_label
    file_list2 = os.listdir(read_path2)
    count_label = 0.0
    add_time = 0.00
    for file_name in file_list2:
        t1 = time.time()
        # basename: all filename in read_path
        basename = os.path.basename(file_name)        
        # name back match
        if basename.endswith('.png') or basename.endswith('.jpg') or basename.endswith('.jpeg'):
            abs_name = read_path2 + file_name
            color_label_img = cv2.imread(abs_name, 1)
            # カラーからラベルへ 変更したカラー画像も生成
            label_img,label_img_change_color = change_label(color_label_img)            
            # 最近傍補間でリサイズ
            label_img_resize = cv2.resize(label_img, (WIDTH, HEIGHT),interpolation=cv2.INTER_NEAREST)
            # バイリニア補間でリサイズ
            label_img_change_color_resize = cv2.resize(label_img_change_color, (WIDTH, HEIGHT))
            cv2.imwrite(parser.output_label + "label_" + file_name, label_img_resize)
            cv2.imwrite(parser.output_color_label + "label_color_" + file_name, label_img_change_color_resize)
            count_label = count_label + 1
            prog = count_label / count_rgb * 100
        t2 = time.time()
        add_time = add_time + (t2 - t1)
        est_time = abs((t2 - t1) * count_rgb - add_time)
        est_time_mod = get_h_m_s(datetime.timedelta(seconds=est_time))
        len_img = len(str(count_rgb_int))
        if count_label < 10:
            print('{} --- {:5.1f}% ({count_label:{len_img}} of {count_rgb:{len_img}}) Time left : Now Estimating...'.format(basename, prog, count_label=int(count_label), len_img=len_img ,count_rgb=int(count_rgb)))
        else:
            print('{} --- {:5.1f}% ({count_label:{len_img}} of {count_rgb:{len_img}}) Time left : {est_time_mod_0:02d}:{est_time_mod_1:02d}:{est_time_mod_2:02d}'.format(basename, prog, count_label=int(count_label), len_img=len_img , count_rgb=int(count_rgb), est_time_mod_0=est_time_mod[0], est_time_mod_1=est_time_mod[1], est_time_mod_2=est_time_mod[2]))

def get_h_m_s(td):
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m ,60)

    return h, m, s


    


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
