import os
import sys
import subprocess
from test.support import interpreters


script = '''
print('Hello world!')
'''


def section_header(label):
    print()
    print('####################')
    print(f'# {label}')
    print('####################')
    print()


#############################

interp = interpreters.create()


#############################

section_header('example 1')

"""
>>> print('Hello world!')
"""

print('Hello world!')


#############################

section_header('example 2')

"""
$ python3 -c "
print('Hello world!')
"
"""

subprocess.run(f'{sys.executable} -c "{script}"', shell=True)


#############################

section_header('example 3')

"""
$ cat << EOF > hello.py
print('Hello world!')
EOF
$ python3 hello.py
"""

with open('hello.py', 'w') as outfile:
    outfile.write(script)
subprocess.run(f'{sys.executable} hello.py', shell=True)
os.unlink('hello.py')


#############################

section_header('example 4')

"""
>>> script = '''
print('Hello world!')
'''
>>> exec(script)
"""

exec(script)


#############################

section_header('example 5')

"""
>>> script = '''
print('Hello world!')
'''
>>> interp.run(script)
"""

interp.run(script)
