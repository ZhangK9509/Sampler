# 数据集采样器
虽然数据集越大越有利于网络模型的训练，但是对于测试代码，尤其是希望完整地运行一边整个训练、评估、测试过程的时候，使用完整的巨大的数据集并不是合适的选择。诚然，手动复制粘贴是可以接受的，但懒惰使我完成了这份代码。

[英文版](./README.md)
# 使用说明
## 安装
1. 克隆或下载并解压本工程。
```
git clone https://github.com/ZhangK9509/sampler
```
2. 根据`requirements.txt`安装依赖包`pyyaml`。
```
pip install -r requirements.txt
```
3. 参考`kitti.yaml`，配置YAML文件。所有的配置文件都保存在`configs`路径下。
### 数据集采样
命令格式如下，可以使用`-h`，阅读帮助文档。
```
python sampler.py <dataset> <dest_dir> <splits> <sample_sizes> [method]
```
例如，要采样数据集`abc`。首先需要配置`abc.yaml`文件。如果需要采样训练数据，样本容量为`10`，那么使用如下命令。采样的数据会被复制到目标路径下，并且生成或更新`train.txt`文件。
```
python sampler.py abc ~/Workspace/Samp/ABC train 10
```
如果采样训练数据和评估数据，样本容量分别为`10`和`4`，那么使用如下命令。除了生成或更新`train.txt`和`val.txt`外，还会生成或更新`trainval.txt`。
```
python sampler.py aBc ~/Workspace/Samp/ABC train,val 10,4
```
默认的采样方法是随机采样。可以通过设定`method`选择顺序采样。
```
python sampler.py ABC ~/Workspace/Samp train 10 --method=SEQUENTIAL
```
允许进行多次采样，但是因为相同的数据会融合，所以最终得到的数据的数量可能比累加的少。
## 欢迎共享你的YAML文件