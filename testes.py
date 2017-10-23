#coding:utf-8
from subprocess import PIPE, Popen
from src.scripts.run_shell import run_shell_scripts
from src.scripts.sh_scripts import *
from sets import Set
import re, csv, json, logging, string
from src.parser import find_patters_commit

def main():
    git = open('git_t.txt')
    lines = git.read()
    print lines.split('\n')[14].replace('\n','')
    print run_shell_scripts(lines.split('\n')[14].replace('\n',''), '')

if __name__ == "__main__":
    main()


# 14