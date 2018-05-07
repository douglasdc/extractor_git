#coding:utf-8

from scripts.run_shell import run_shell_scripts
from scripts.sh_scripts import get_first_commit

def david_ma(since, until, files, regex, amount):
    import progressbar
    barA = progressbar.ProgressBar()
    barM = progressbar.ProgressBar(max_value=len(
        regex_list) * len(files))
    global commitsObj
    global developers
    commits2 = {}

    print 'Buscando commits de arquivos pela lista de metodos.....'
    # tat = '\(|.'.join(map(str, regex_list))
    i = 0
    j = 0
    for file in files:
        i = i + 1
        k = 100 * i / len(files)
        # barA.update(k)
        #Hashs dos commits que usaram o atributo nesse arquivo
        # print i
        for tat in regex_list:
            j = j + 1
            barM.update(j)
            # print str(i) + '/43' + '-----' + str(j)
            commit_hash = run_shell_scripts(commit_sha1_by_regex_file(
                tat, file, git_path, SINCE, UNTIL), '')
            # print commit_hash
            if len(commit_hash) > 0:
                commits = strip_data_commit(commit_hash)
                for commit in commits:

                    if commit[0] not in id_commit_method:
                        id_commit_method[commit[0]] = []

                    if commit[0] not in commits:
                        temp = {}
                        temp['commit'] = commit[0]
                        if 'Maurício' in commit[1] or 'Mauricio' in commit[1]:
                            temp['autor'] = 'Mauricio'
                        elif 'Barry' in commit[1] or 'bcron10' in commit[1]:
                            temp['autor'] = 'Barry Cronin'
                        else:
                            temp['autor'] = commit[1]
                        temp['timestamp'] = commit[2]
                        temp['email'] = commit[3]
                        temp['metodos'] = []
                        temp['arquivos'] = []
                        temp['arquivos'].append(file)

                        commits2[commit[0]] = temp
                    else:
                        commits2[commit[0]]['arquivos'].append(file)

    info_file('output/commits_atributos.txt', id_commit_method)
    print 'Encontrato ' + str(len(commits2)) + ' commits'
    return commits2
    
