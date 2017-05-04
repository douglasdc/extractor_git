#coding:utf-8
log = 'git log'

log_to_file = lambda file:'git log --pretty=fuller --stat ' + file

all_contribuitors_name = "git log --pretty='%an' | sort | uniq"

author_commit_sha1 = lambda sha1: 'git show -s --format=%an ' + sha1
timestamp_commit_sha1 = lambda sha1: 'git show -s --format=%at ' + sha1

count_commits = 'git rev-list --count master'

count_contribuitors = 'git shotlog -s -n --all | wc -l'

count_commit_all_contributors = 'git shortlog -s -n --all master'

commit_regex = lambda regex:'git log --follow -S' + '"' + regex + '"' + ' --pretty=fuller .'
# commit_regex = lambda regex:'git log --follow -S' + '"' + regex + '"' + '--pretty=fuller .'

# Nome dos autores dos commites de determinado aquivo que casam com o padrão regex
commit_regex_by_author = lambda regex, file:'git log --follow -S' + '"' + regex + '"' + ' --pretty=format:%an ' + file

see_changed_files = lambda file_type:'git diff-tree --no-commit-id --name-only -r | awk "/^.*\.' + file_type + '/'

commit_sha1_by_file = lambda file_path:'git log --format=format:%H ' + file_path

commit_sha1_by_regex = lambda regex:'git log --follow -S' + '"' + regex + '"' + ' --format=format:%H .'

commit_sha1_by_regex_file = lambda regex, file_path:'git log --follow -S' + '"' + regex + '"' + ' --format=format:%H ' + file_path

commited_files = lambda sh1a, file_type:'git diff-tree --no-commit-id --name-only -r ' + sh1a +' | awk "/^.*\.' + file_type + '/"'
# commited_files = lambda sh1a, file_type:'git diff-tree --no-commit-id --name-only -r d00ebd640d699b33de06b759b4ee219fa9f3e46a | awk "/^.*\.java/"'