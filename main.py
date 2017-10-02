#coding:utf-8
from src.main import primeiro
import logging

def main():
    import sys
    # sys.path.append('/')
    
    primeiro()

if __name__ == "__main__":
    logging.basicConfig(filename='output/logs.log',level=logging.DEBUG)
    main()