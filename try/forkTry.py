import subprocess

print('$ nslookup')
p = subprocess.Popen(['python3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'1+1\nexit\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)
