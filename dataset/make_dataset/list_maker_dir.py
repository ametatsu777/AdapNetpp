#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys
import argparse

def main():
	##how_to use##
	# dir付きバージョン
	# $python list_maker.py -hでオプション確認
	# -i 入力となる画像が入っているディレクトリ　-l　正解ラベル画像が入っているディレクトリ　-o txtファイル保存場所
	# 例：$python list_maker.py -i /rgb_image/ -l /label_image/ -o ../../list_train.txt

	#             $python list_maker.py <RGBimages path> <label images path> <to write path(.txt)>
	txtfiles_depth = []
	txtfiles_label = []
	dir_array = []


	# dir RGBimages
	read_path1 = parser.input_img
	for dir in os.listdir(read_path1):
		if os.path.isdir(os.path.join(read_path1, dir)):
			data_dir_path = read_path1 + dir
			file_list1 = os.listdir(read_path1 + '/' + dir)
			print('[' + dir + ']')
			print('\n')

			for file_name1 in file_list1:
				# basename: all filename in read_path
				basename1 = os.path.basename(file_name1)
				print(basename1)
				if basename1.endswith('.png'):
					txtfiles_depth.append(basename1)
			txtfiles_depth.sort()
			print('\n')

	# dir labelImages
	read_path2 = parser.label_img
	for dir in os.listdir(read_path2):
		if os.path.isdir(os.path.join(read_path2, dir)):
			data_dir_path = read_path2 + dir
			file_list2 = os.listdir(read_path2 + '/' + dir)
			print('[' + dir + ']')
			print('\n')

			for file_name2 in file_list2:
				# basename: all filename in read_path
				basename2 = os.path.basename(file_name2)
				print(basename2)
				if basename2.endswith('.png'):
					txtfiles_label.append(basename2)
					dir_array.append(dir)
			txtfiles_label.sort()
			print('\n')
			
			print('Images number:'),
			print(len(txtfiles_depth))
			print('labelImages number:'),
			print(len(txtfiles_label))
			
	# write to txt file
	# 追記'a'  上書き'w'
	write_path = parser.output
	f = open(write_path,'w')
	dir_array.sort()
	for i in range(len(txtfiles_depth)):
		f.write(read_path1)
		f.write(dir_array[i])
		f.write('/')
		f.write(txtfiles_depth[i])
		f.write(' ')

		f.write(read_path2)
		f.write(dir_array[i])
		f.write('/')
		f.write(txtfiles_label[i])
		f.write('\n')

		i += 1
	f.close()

def get_parser():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-i', '--input_img', help='input_image_dir')
    parser.add_argument('-l', '--label_img', help='label_image_dir')
    parser.add_argument('-o', '--output', help='output_txt_dir')
    return parser


if __name__ == '__main__':
    parser = get_parser().parse_args()
    main()
