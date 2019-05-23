# Sampler: Take a sample of your dataset
Although larger the dataset it is, better training will be, large dataset is not approprate for testing/debuging codes. A small set of data is needed to just make sure codes can work well. This sampler is a such thing which takes a sample of the dataset.

[中文版](./README_CN.md)
## Quick Start
### Installation
1. Clone the repository.
```
git clone https://github.com/ZhangK9509/sampler
```
2. Install pyyaml, the only requirement.
```
pip install -r requirements.txt
```
3. Do configure. YAML file is needed. Write your YAML file in directory `configs`. A sample about Kitti dataset has been given for reference.
### Sampling
Command is as follows. Use `-h` for more help.
```
python sampler.py <dataset> <dest_dir> <splits> <sample_sizes> [method]
```
For an example, to take a sample of dataset `abc`, a YAML file named `abc.yaml` is essential. If data for training is wanted, use command as follows and data will be copied to the destination directory with a file named `train.txt` which records data's ID numbers.The sample size is `10`.
```
python sampler.py abc ~/Workspace/Samp/ABC train 10
```
If data for training and validating is wanted, use command as follows and data will be copied to the destination directory with files `train.txt`, `val.txt` and `trainval.txt`. The sample sizes are `10` and `4`.
```
python sampler.py aBc ~/Workspace/Samp/ABC train,val 10,4
```
Default sampling method is random sampling. In addition, sequential sampling is available.
```
python sampler.py ABC ~/Workspace/Samp train 10 --method=SEQUENTIAL
```
Multiple samplings are allowed. Data will be merged. And the total number could be less than accumulation because only one data will be retained if two are the same.
## Contributing to the project
Sharing your YAML files and any pull requests or issues are welcome.
## About `521` and `522`
`520`, `521` and `522` are gifts send by Chinese. In Chinese, `520` and `521` share a similar pronunciation with `我爱你` (I love you). `522` if as a hexadecimal number equals to 1314, a decimal number which shares a similar pronumciation with `一生一世` (forever) in Chinese. Read together, `5201314` means I love you forever.