#! /usr/bin/python3
import os
import sys
import subprocess
from threading import Thread
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
    socket_print("cleaning")
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
    copy("/home/ctf/trans_asm", filename+"/trans_asm")
    copy("/home/ctf/trans_IR", filename+"/trans_IR")
    copy("/home/ctf/inter.txt", filename+"/inter.txt")
    copy("/home/ctf/test.c", filename+"/test.c")

def check(filename):
    while True:
        if sys.stdout.closed:
            clean_file(filename)
            socket_print("Cleaned up directory:")

def main():
    filename = get_filename()
    Thread(target=check,args=filename)
    copy_file(filename)
    run_challenge(filename)
    clean_file(filename)

if __name__ == "__main__":
    main()