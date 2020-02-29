# mysharelib

## 使用方法

克隆仓库：

```bash
git clone https://github.com/hongweiniu/mysharelib.git
```

可以把仓库放到一个地方，每次用之前pull一下，保证代码是最新版。

```bash
cd /some/mysharelib
git pull
```

然后实际用的时候要把mysharelib所在目录加到PYTHONPATH环境变量

```bash
export PYTHONPATH=/some:$PYTHONPATH
```

当然，也可以把这个语句直接加到.bashrc

调用库：

```python
from mysharelib import mymath
from mysharelib.mymath import *
```

建议用第一种方式，不然不安全。

## 脚本和函数说明

### mymath.h

一些包装好的数学函数

#### mymath.cal_mae

```python
mymath.cal_mae(a, b)
```

参数：a, b（一维numpy array）

返回值：Mean Absolute Error

#### mymath.cal_rmse

参数：a, b（一维numpy array）

返回值：Root Mean Squared Error

#### mymath.cal_r2

参数：a, b（一维numpy array）

返回值：相关系数

#### mymath.cal_se

参数：a（一维numpy array）

返回值：标准误差