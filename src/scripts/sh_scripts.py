#coding:utf-8

import logging, datetime
from sys import platform

DEFINE_GIT_FOLDER = lambda git_folder: 'git -C ' + git_folder + ' '
DEFINE_PERIOD = lambda since, until: '--since "' +  since.isoformat() + '" --until "' + until.isoformat() + '"'

def log(git_folder): 
    return DEFINE_GIT_FOLDER(git_folder)(git_folder) + ' log'


def log_to_file(file, git_folder): 
    script = DEFINE_GIT_FOLDER(git_folder) + ' log --pretty=fuller --stat ' + file
    logging.info(script)
    return script


def all_contribuitors_name(git_folder): 
    script = DEFINE_GIT_FOLDER(git_folder) + " log --pretty='%an' | sort | uniq"
    logging.info(script)
    return script


def author_commit_sha1(sha1, git_folder): 
    script = DEFINE_GIT_FOLDER(git_folder) + ' show -s --format=%an ' + sha1
    logging.info(script)
    return script


def timestamp_commit_sha1(sha1, git_folder): 
    script = DEFINE_GIT_FOLDER(git_folder) + ' show -s --format=%at ' + sha1
    logging.info(script)
    return script


# def count_commits(git_folder): 
#     script = DEFINE_GIT_FOLDER(git_folder) + ' rev-list --count master'
#     logging.info(script)
#     return script


def count_contribuitors(git_folder): 
    script = DEFINE_GIT_FOLDER(git_folder) + ' shotlog -s -n --all | wc -l'
    logging.info(script)
    return script


def count_commit_all_contributors(git_folder): 
    script = DEFINE_GIT_FOLDER(git_folder) + ' shortlog -s -n --all master'
    logging.info(script)
    return script


def commit_regex(regex, git_folder): 
    script = DEFINE_GIT_FOLDER(git_folder) + ' log --follow -S' + '"' + regex + '"' + ' --pretty=fuller .'
    logging.info(script)
    return script


def commit_regex_by_author(regex, file, git_folder): 
    script = DEFINE_GIT_FOLDER(git_folder) + ' log --follow -S' + '"' + regex + '"' + ' --pretty=format:%an ' + file
    logging.info(script)
    return script


def see_changed_files(file_type, git_folder): 
    languages = '|'.join(map(str, file_type))
    script = DEFINE_GIT_FOLDER(git_folder) + ' diff-tree --no-commit-id --name-only -r | awk "/^.*\.(' + languages + ')/"'
    
    logging.info(script)

    return script


def commit_sha1_by_file(file_path, git_folder, since=datetime.date(1990, 1, 1), until=datetime.date(2030, 1, 1)):
    script = DEFINE_GIT_FOLDER(
        git_folder) + ' log ' + DEFINE_PERIOD(since, until) + ' --format=format:%H -- ' + file_path
    
    logging.info(script)

    return script


def commit_sha1_by_regex(regex, git_folder, since=datetime.date(1990, 1, 1), until=datetime.date(2030, 1, 1)):
    script = DEFINE_GIT_FOLDER(git_folder) + ' log ' + DEFINE_PERIOD(since, until) + ' --follow -G' + '"' + regex + '"' + ' --format=format:"%H|%an|%at" -- .'
    logging.info(script)

    return script


def commit_sha1_by_regex_file(regex, file_path, git_folder, since=datetime.date(1990,1,1), until=datetime.date(2030,1,1)):
    script = DEFINE_GIT_FOLDER(git_folder) + ' log ' + DEFINE_PERIOD(since, until) + ' --follow -G' + '".' + regex + '\("' + ' --format=format:"%h|%an|%at|%ae" -- ' + file_path
    
    logging.info(script)
    
    return script


def commited_files(sh1a, file_type, git_folder): 
    languages = '|'.join(map(str, file_type))
    script = DEFINE_GIT_FOLDER(git_folder) + ' show --pretty="" --name-only ' + sh1a + ' | awk "/^.*\.(' + languages + ')/"'

    logging.info(script)

    return script


def get_all_commit(sh1a, file_path, git_folder):
    script = DEFINE_GIT_FOLDER(git_folder) + ' show ' + sh1a + ' ' + file_path
    
    logging.info(script)

    return script

def get_amount_commits(regex, file_path, git_folder, since=datetime.date(1990,1,1), until=datetime.date(2030,1,1)):
    from datetime import timedelta

    script = DEFINE_GIT_FOLDER(git_folder) + ' log -1  --follow -G' + '".' + regex + '\("' + ' --format=format:"%h|%an|%at|%ae" -- ' + file_path 
    logging.info(script)

    return script

def get_all_files(git_path, regex, sh1a):
    script = 'git -C ' + git_path + ' show --pretty="" -G' + '"' + regex + '"' + ' --no-commit-id --name-only -r ' + sh1a
    logging.info(script)
    return script

def search_for_single_file(git_path, file):
    script = ''
    if platform == 'linux' or platform == 'linux2':
        script = '[ -f "' + git_path + '/' + file + '" ] && echo "Arquivo existe"'
    else:
        script = '[ -f "' + git_path + '/' + file + '" ] && echo "Arquivo existe"'

    return script

def tt(git_path, since=datetime.date(1990,1,1), until=datetime.date(2030,1,1)):
    script = DEFINE_GIT_FOLDER(git_path) + ' log ' + DEFINE_PERIOD(since, until) + ' --pretty=format:"##--##commit|%h|%an|%at|%ae" -p --reverse'
    # print(script)
    return script