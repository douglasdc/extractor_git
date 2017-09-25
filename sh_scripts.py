#coding:utf-8
def log(git_folder): 
    return 'git -C ' + git_folder + ' log'


def log_to_file(file, git_folder): 
    return 'git -C ' + git_folder + ' log --pretty=fuller --stat ' + file


def all_contribuitors_name(git_folder): 
    return "git -C " + git_folder + " log --pretty='%an' | sort | uniq"


def author_commit_sha1(sha1, git_folder): 
    return 'git -C ' + git_folder + ' show -s --format=%an ' + sha1


def timestamp_commit_sha1(sha1, git_folder): 
    return 'git -C ' + git_folder + ' show -s --format=%at ' + sha1


def count_commits(git_folder): 
    return 'git -C ' + git_folder + ' rev-list --count master'


def count_contribuitors(git_folder): 
    return 'git -C ' + git_folder + ' shotlog -s -n --all | wc -l'


def count_commit_all_contributors(
    git_folder): return 'git -C ' + git_folder + ' shortlog -s -n --all master'


def commit_regex(regex, git_folder): 
    return 'git -C ' + git_folder + ' log --follow -S' + '"' + regex + '"' + ' --pretty=fuller .'
# commit_regex = lambda regex:'git log --follow -S' + '"' + regex + '"' + '--pretty=fuller .'

# Nome dos autores dos commites de determinado aquivo que casam com o padrão regex


def commit_regex_by_author(regex, file, git_folder): 
    return 'git -C ' + git_folder + ' log --follow -S' + '"' + regex + '"' + ' --pretty=format:%an ' + file


def see_changed_files(file_type, git_folder): 
    return 'git -C ' + git_folder + ' diff-tree --no-commit-id --name-only -r | awk "/^.*\.' + file_type + '/'


def commit_sha1_by_file(file_path, git_folder): 
    return 'git -C ' + git_folder + ' log --format=format:%H ' + file_path


def commit_sha1_by_regex(regex, git_folder): 
    return 'git -C ' + git_folder + ' log --follow -S' + '"' + regex + '"' + ' --format=format:%H .'


def commit_sha1_by_regex_file(regex, file_path, git_folder): 
    print 'git -C ' + git_folder + ' log --follow -S' + '"' + regex + '"' + ' --format=format:%H ' + file_path
    return 'git -C ' + git_folder + ' log --follow -S' + '"' + regex + '"' + ' --format=format:%H ' + file_path


def commited_files(sh1a, file_type, git_folder): 
    return 'git -C ' + git_folder + ' diff-tree --no-commit-id --name-only -r ' + sh1a + ' | awk "/^.*\.' + file_type + '/"'
# commited_files = lambda sh1a, file_type:'git diff-tree --no-commit-id --name-only -r d00ebd640d699b33de06b759b4ee219fa9f3e46a | awk "/^.*\.java/"'
