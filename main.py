#coding:utf-8
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
