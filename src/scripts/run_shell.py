# coding:utf-8

# Executa scripts shell e retorna sua saída
def run_shell_scripts(script, folder):
    from subprocess import PIPE, Popen
    
    # result = subprocess.call(['git log'], shell=True)
    p = Popen(script, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    
    output, err = p.communicate()
    rc = p.returncode
    # print(output)
    return output.decode('utf-8', errors="ignore")
