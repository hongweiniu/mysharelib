# 使用方法

克隆仓库：

```bash
cd /.../some
git clone https://github.com/hongweiniu/mysharelib.git
```

可以把仓库放到一个地方，每次用之前pull一下，保证代码是最新版。

```bash
cd /.../some/mysharelib
git pull
```

然后实际用的时候要把mysharelib所在目录加到PYTHONPATH环境变量

```bash
export PYTHONPATH=/.../some/mysharelib:$PYTHONPATH
```

当然，也可以把这个语句直接加到.bashrc

调用模块例子：

```python
from mytool import myio
myio.atoms2data(atoms, 'data.txt')
```
