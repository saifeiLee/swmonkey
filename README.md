# 基于 pyautogui 的 Monkey 测试工具

## 运行

1. 进入 venv 环境

```
source venv/bin/activate
```

2. 安装依赖

```
pip install -r requirements.txt
```

3. 本地安装

```
pip install -e .
```

4. 执行命令

```
swmonkey -d 60 # 运行60秒
```

## 安装

```
pip install --index-url https://pypi.org/project swmonkey --upgrade
```

## 使用

设置环境变量

```
export XDG_CURRENT_DESKTOP=UKUI
```

## 参数

### swmonkey

**-d**

指定运行时间

**-r**

以回放模式运行，需要搭配`-p` 参数指定回访数据的路径

**-p**

指定回放数据的路径。回放数据和日志的路径默认在 `~/.swmonkey/`下。例如：

```
swmonkey -d 20 -r -p  ~/.swmonkey/20230911114348/actions.json # 回放 ~/.swmonkey/20230911114348/actions.json的数据
```

### swmonkey_runner

`swmonkey_runner`以多进程的方式运行`swmonkey`, 目的是在 swmonkey 进程挂掉的时候，可以自动重启

**--keep-alive**

启用后, smwonkey 服务会检测系统 CPU 和内存占用,通过终止一些应用进程来保证系统正常运行

**--interval [int]**

指定 GUI 操作的间隔时间, 单位为秒, 默认为 0.5 秒

**--app-path [App Launch Path]**

启动应用，并把 monkey 测试限定在应用窗口范围内。例如`swmonkey_runner  -d 600000 --app-path /usr/bin/firefox  --keep-alive`

**--restart-x11**

开启这个参数，会在 swmonkey 挂掉的时候，自动重启 X11 服务，前提是终端需要配置了自动运行 monkey, 如何配置参见:https://kb.cvte.com/pages/viewpage.action?pageId=377734914

**--password [string]**

指定 sudo 密码，用于 swmonkey 进程挂掉的时候，自动重启 X11 服务

### 特别说明
当前存在两种方法用于smwonkey保活：


**方法一**: 开机自启动的方式,

 [配置开机自启](https://kb.cvte.com/pages/viewpage.action?pageId=377734914)后，使用命令启动monkey测试:
```
systemctl restart lightdm
```


**方法二**: 使用`--keep-alive`参数 (推荐)
```
export XDG_CURRENT_DESKTOP=UKUI
swmonkey_runner -d 600000 --keep-alive
```

## 设计文档

https://kb.cvte.com/pages/viewpage.action?pageId=372571592

## 构建和发布

```
./auto-upload.sh

# 构建/发布混淆版本的包
# 注意: 使用混淆版本的包，终端的python版本需要与构建环境一致(3.10.7)
./auto-upload.sh --armor
```

### 注意

1. 需要先安装 twine

```
pip install twine
```

2. 需要配置 pypi 账号,配置文件路径为 ~/.pypirc

参考

```
[distutils]
index-servers =
    pypi

[pypi]
usernam = __token__
password = YOUR_TOKEN
```

## 本地测试

```
python -m venv venv

source venv/bin/activate

pip install -e . # Install package in editable mode

swmonkey -d 15 # Run 15 seconds
# 查看日志文件, 日志文件和录制文件都在 ~/.swmonkey/ 目录下，目录名为时间戳
ls ~/.swmonkey/
```
