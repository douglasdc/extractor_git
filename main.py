#!/usr/bin/env python3
#coding:utf-8
import sys
# importlib.reload(sys)
# sys.setdefaultencoding('utf8')

from src.main import start_extraction
import logging
from datetime import datetime


def main():

    start_extraction()

if __name__ == "__main__":
    data = datetime.now()
    file_name = "output/logs/log-{:%d_%m_%y-%H_%M_%S}.log".format(data)
    logging.basicConfig(filename=file_name,level=logging.DEBUG)
    main()
