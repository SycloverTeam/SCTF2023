#! /usr/bin/python3
import os
import sys
import subprocess
from shutil import copy
import uuid

def socket_print(string):
    print("=====", string, flush=True)

def run_challenge(filename):
    socket_print("Testing edge compute app...")
    try: 
        result = subprocess.run(filename+"/trans_IR",shell=True, timeout=60)
    except subprocess.CalledProcessError as e:
        socket_print("stopping")
        clean_file(filename)
        pass
    socket_print("Test complete!")

def get_filename():
    return "/home/ctf/tmp/{}".format(uuid.uuid4().hex)

def clean_file(filename):
    result = subprocess.run("rm -r "+filename, shell=True, timeout=10)

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                  
		os.makedirs(path)          
		socket_print("OK")
	else:
		socket_print("There is this folder!")

def copy_file(filename):
    mkdir(filename)
    copy("./trans_asm", filename+"/trans_asm")
    copy("./trans_IR", filename+"/trans_IR")
    copy("./inter.txt", filename+"/inter.txt")
    copy("./test.c", filename+"/test.c")

def main():
    try:
        filename = get_filename()
        copy_file(filename)
        run_challenge(filename)
        clean_file(filename)
    except KeyboardInterrupt:
        clean_file(filename)

if __name__ == "__main__":
    main()