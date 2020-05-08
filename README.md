# AdapNet++_3class[編集中]


## 環境依存
* Python2
* tensorflow-gpu1.10.0
* pyyaml

## 準備
dockerを使用するのがオススメです。
### dockerを使用する場合
dockerがインストールされていることが前提です。  
また、dockerが保存されている/t_dataはマウントし、ホームディレクトリ直下にshared_dirを作成しておいてください。  
	
1. コードのダウンロード  
dockerとやり取りするためshared_dir内にコードをダウンロードしてください。
```
cd /home/shared_dir
git clone http://data.tasakilab:8080/gitbucket/git/amemiya/AdapNet++_3class.git
cd AdapNet++_3class
rm -r -f .git
```
.gitを消しているのは、初心者が誤ってgitbucketのソースコードを変更しないようにするためです。  

2. dockerイメージの展開  
```
sudo docker load < /t_data/docker/tensorflow-tensorflow__1.10.0-gpu-py2-pythontk-yaml-cv2.tar
```
3. dockerコンテナの起動  
nvidia-dockerをdockerで使えるようにする
```
sudo apt install nvidia-container-toolkit
```
コンテナ作成・起動 
```
docker run --gpus all -it -v ~/shared_dir/AdapNet++_3class:/root/shared_dir tensorflow-tensorflow__1.10.0-gpu-py2-pythontk-yaml-cv2
```
一度起動したコンテナに再び入るとき  
```
docker start [コンテナ名]
docker attach [コンテナ名]
```
※コンテナ名は$docker ps -aで確認できる。  

## 使い方

### データセット整備

1. リスト作成

	```
	[入力画像パス1] [ラベル画像パス1]
	[入力画像パス2] [ラベル画像パス2]
	[入力画像パス3] [ラベル画像パス3]
	...

	```
参考：dataset/make_dataset/list_maker.py  
　　 (txtファイルを作れます。使い方はコード内に記述してあります。)
2. tfrecord作成
```
python convert_to_tfrecords.py -f [リストファイル(.txt)パス] -r [tfrecordファイル(.records)パス]
```


### 学習
1. configファイル編集
2. 学習
```
python train_tensorboard.py -c [configファイル]
```

### 評価
1. configファイル編集
2. 評価  
	12クラス
	```
	python evaluate_12label.py -c [configファイル] -d [保存場所]
	```
	

	3クラス
	```
	python evaluate_3label.py -c [configファイル] -o [出力画像保存場所] -p [確信度マップ保存場所]
	```
	※-o -pは保存したい場合のみ  
	
### TensorBoard
```
tensorboard --logdir=[logsディレクトリ]
```
※logsフォルダは複数あるとダメです。

### configファイル編集方法
#### 学習パラメータ
```
    gpu_id: id of gpu to be used(マルチGPUでなければ'0')
    model: name of the model
    num_classes: number of classes (including void, label id:0)
    intialize:  path to pre-trained model('init_checkpoint/AdapNet_pp_init.ckpt')
    checkpoint: path to save model
    train_data: path to dataset .tfrecords
    batch_size: training batch size
    skip_step: how many steps to print loss 
    height: height of input image
    width: width of input image
    max_iteration: how many iterations to train
    learning_rate: initial learning rate
    save_step: how many steps to save the model
    power: parameter for poly learning rate(? 0.001ぐらいでやってます)
```

#### 評価パラメータ
```
    gpu_id: id of gpu to be used(マルチGPUでなければ'0')
    model: name of the model
    num_classes: number of classes (including void, label id:0)
    checkpoint: path to saved model
    test_data: path to dataset .tfrecords
    batch_size: evaluation batch size
    skip_step: how many steps to print mIoU
    height: height of input image
    width: width of input image
```
※例：example.config

### 注意点
クラス0は後塗りで評価しています。
クラス0の後塗りを無くしたい場合はevaluateファイルの
```
prediction[gt == 0] = 0
```
をコメントアウトしてください。
# AdapNetpp
