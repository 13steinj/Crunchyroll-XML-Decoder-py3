#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from time import sleep
from urllib.parse import urlparse
from configparser import ConfigParser
import pickle
import requests
import cfscrape
from lxml import etree
import json
from unidecode import unidecode

from urllib.request import url2pathname
import os
import psutil
import wget
import zipfile
import math
import shutil
import subprocess

def idle_cmd_txt_fix(print_text):
    if 'idlelib.run' in sys.modules:
        print_text = re.sub('\\x1b.*?\[\d*\w','',print_text)
    return print_text

if os.path.lexists(os.path.join('.', 'crunchy-xml-decoder-py3.py')):
    code_dir__ = os.path.join(".", "")
elif os.path.lexists(os.path.join('..', 'crunchy-xml-decoder-py3.py')):
    code_dir__ = os.path.join("..", "")
else:
    print(idle_cmd_txt_fix('\x1b[31m' + "Can't find the crunchy-xml-decoder-py3 Folder" + '\x1b[0m'))


def get_lastest_version():
    version_url = 'https://raw.githubusercontent.com/alzamer2/Crunchyroll-XML-Decoder-py3/master/VERSION'
    github_version = requests.get(version_url).text
    github_version_parse = re.findall(r'(\d+)\.(\d+) rev\.(\d+)',github_version.split('\n')[0].replace('#',''))[0]
    locale_version = open(os.path.join(code_dir__,'VERSION'),'r').readlines()
    locale_version_parse = re.findall(r'(\d+)\.(\d+) rev\.(\d+)', locale_version[0].replace('#',''))[0]
    return [github_version_parse, locale_version_parse]

def close_code():
    print('trying to close Crunchyroll-XML-Decoder-py3.......')
    for proc in psutil.process_iter():
        pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
        if pInfoDict['name'] == 'python.exe' or pInfoDict['name'] == 'pythonw.exe' :
            if len(pInfoDict['cmdline']) > 1:
                #print(os.path.split(os.path.normpath(pInfoDict['cmdline'][1]))[0],os.path.normpath(os.path.abspath(code_dir__)))
                if os.path.split(os.path.normpath(pInfoDict['cmdline'][1]))[0] == os.path.normpath(os.path.abspath(code_dir__)):
                    #print(os.path.split(os.path.split(pInfoDict['cmdline'][1])[0])[1])
                    #print(pInfoDict)
                    p = psutil.Process(pInfoDict['pid'])
                    p.terminate()
                    p.wait()

def unzip_(filename_,out):
    zf = zipfile.ZipFile(filename_)
    uncompress_size = sum((file.file_size for file in zf.infolist()))
    extracted_size = 0
    for file in zf.infolist():
        extracted_size += file.file_size
        percentage = extracted_size * 100/uncompress_size
        avail_dots = 73
        shaded_dots = int(math.floor(float(extracted_size) / uncompress_size * avail_dots))
        sys.stdout.write("\r" + '[' + '*'*shaded_dots + '-'*(avail_dots-shaded_dots) + '] %'+str(int(percentage)))
        zf.extract(file,out)
    sys.stdout.write('\n')

def run_update():
    code_version = get_lastest_version()
    if code_version[1] < code_version[0]:
        close_code()
        wget.download('https://github.com/alzamer2/Crunchyroll-XML-Decoder-py3/archive/master.zip',os.path.abspath(os.path.join(code_dir__,'update.zip')))
        unzip_(os.path.abspath(os.path.join(code_dir__,'update.zip')),os.path.abspath(os.path.join(code_dir__,'update')))
        root_dir = os.path.join(code_dir__,'update','Crunchyroll-XML-Decoder-py3-master')
        for path, subdirs, files in os.walk(root_dir):
            for name in files:
                shutil.move(os.path.join(os.path.abspath(path),name),os.path.join(os.path.abspath(code_dir__),os.path.relpath(path, root_dir),name))
        os.remove(os.path.abspath(os.path.join(code_dir__,'update.zip')))
        shutil.rmtree(os.path.join(code_dir__,'update'))
        subprocess.call([sys.executable.replace('pythonw.exe', 'python.exe'),
                         os.path.join(code_dir__, "crunchy-xml-decoder-py3.py")])


if __name__ == '__main__':
    run_update()
    #print(get_lastest_version()[0][:2])
