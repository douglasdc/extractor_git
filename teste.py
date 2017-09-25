from subprocess import PIPE, Popen

# result = subprocess.call(['git log'], shell=True)
script = ['git log /mnt/c/Users/Douglas/Downloads/Documents']
p = Popen(script, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

output, err = p.communicate()
rc = p.returncode
print err
print output
