# mysharelib

## 使用方法

```bash
git clone https://github.com/hongweiniu/mysharelib.git
```

```python
from mysharelib import *
from mysharelib import mymath
```

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