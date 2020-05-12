# AdapNet++_勉強会


## 環境依存
* Python2
* tensorflow-gpu1.10.0
* pyyaml


## 準備
dockerを使用するのがオススメです。dockerのインストール方法は各自調べてください。
### dockerを使用する場合
dockerがインストールされていることが前提です。  
dockerイメージをダウンロードしてホームディレクトリ直下においてください。(OneDrive/ファイル/Meeting/2020/移動ロボット/雨宮/勉強会/tensorflow-tensorflow__1.10.0-gpu-py2-pythontk-yaml-cv2.tar)  
また、ホームディレクトリ直下にshared_dirを作成しておいてください。  
	
1. コードのダウンロード  
dockerとやり取りするためshared_dir内にコードをダウンロードしてください。
```
cd $HOME/shared_dir
git clone https://github.com/ametatsu777/AdapNetpp.git
rm -r -f .git
```
.gitを消しているのは、初心者が誤ってgitbucketのソースコードを変更しないようにするためです。  

2. dockerイメージの展開  
```
sudo docker load < ~/tensorflow-tensorflow__1.10.0-gpu-py2-pythontk-yaml-cv2.tar
```
3. dockerコンテナの起動  
nvidia-dockerをdockerで使えるようにする
```
sudo apt install nvidia-container-toolkit
```
コンテナ作成・起動 
```
docker run --gpus all -it -v ~/shared_dir/AdapNetpp:/root/shared_dir tensorflow-tensorflow__1.10.0-gpu-py2-pythontk-yaml-cv2
```
マウントしたファイルのowner問題解決(root→User)したいのであれば(こちらの方がおすすめ)  
```
docker run --gpus all -it -v ~/shared_dir/AdapNetpp:/root/shared_dir -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro -u 1000:1000 tensorflow-tensorflow__1.10.0-gpu-py2-pythontk-yaml-cv2
```
※-uのオプションは一例　$idコマンドでuidとgidを調べてください。$(id -u $USER):$(id -g $USER)でも可。  

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
	python evaluate_12label.py -c [configファイル] -d [出力結果保存場所]
	```
	
	※-d -pは保存したい場合のみ  
	
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

