from threading import Thread
import interpreters


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
>>> def task():
...     print('Hello world!')
...
>>> t = Thread(target=task)
>>> t.start()
"""

def task():
    print('Hello world!')

t = Thread(target=task)
t.start()
t.join()


#############################

section_header('example 2')

"""
>>> script = '''
print('Hello world!')
'''
>>> t = Thread(target=exec, args=(script,))
>>> t.start()
"""

t = Thread(target=exec, args=(script,))
t.start()
t.join()


#############################

section_header('example 3')

"""
>>> script = '''
print('Hello world!')
'''
>>> t = Thread(target=interp.run, args=(script,))
>>> t.start()
"""

t = Thread(target=interp.run, args=(script,))
t.start()
t.join()


#############################

section_header('example 4')

"""
>>> script = '''
print('Hello world!')
'''
>>> def task():
...     interp = interpreters.create()
...     interp.run(script)
...
>>> Thread(target=task).start()
"""

def task():
    interp = interpreters.create()
    interp.run(script)

t = Thread(target=task)
t.start()
t.join()
