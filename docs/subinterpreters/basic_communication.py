# to run on command line to see result, not on IDLE
import os
import os.path
import pickle
from threading import Thread
import interpreters


SCRIPT_DIR = os.path.dirname(__file__)


def section_header(label):
    print()
    print('####################')
    print(f'# {label}')
    print('####################')
    print()


#############################

interp = interpreters.create()

interp.run(f'''if True:
    def get_question(answer):
        return '<question for {{}}>'.format(answer)
    ''')

interp.run(f'''if True:
    import os
    import pickle

    def handle_data(data):
        print('handling data: {{!r}}'.format(data))
    ''')


#############################

section_header('example 1')

"""
>>> data1, data2 = 42, 'spam'
>>> interp.run(f'''if True:
...     q = get_question({data1})
...     write(q)
...     write({data2!r})
...     ''')
"""

data1, data2 = 42, 'spam'
interp.run(f'''if True:
    q = get_question({data1})
    print(q)
    print({data2!r})
    ''')


#############################

section_header('example 2')

"""
>>> r, w = os.pipe()
>>> def handler():
...     interp.run(f'''if True:
...         handle_data( os.read({r}, 100) )
...         ''')
...
>>> Thread(target=handler).start()
>>> os.write(w, b'spam')
"""

r, w = os.pipe()

def handler():
    interp.run(f'''if True:
        data = os.read({r}, 100)
        handle_data(data)
        ''')

t = Thread(target=handler)
t.start()

os.write(w, b'spam')

t.join()
os.close(r)
os.close(w)


#############################

section_header('example 3')

"""
>>> r, w = os.pipe()
>>> r2, w2 = os.pipe()
>>> def handler():
...     interp.run(f'''if True:
...         data = os.read({r}, 100)
...         while True:
...             handle_data(data)
...             os.write({w2}, b'<ACK>')
...             data = os.read({r}, 100)
...         ''')
...
>>> Thread(target=handler).start()
>>> os.write(w, b'spam')
>>> os.read(r2, 100)
"""

r, w = os.pipe()
r2, w2 = os.pipe()

def handler():
    interp.run(f'''if True:
        data = os.read({r}, 100)
        while data != b'<DONE>':
            handle_data(data)
            os.write({w2}, data)
            data = os.read({r}, 100)
        print('handler done!')
        ''')

t = Thread(target=handler)
t.start()

os.write(w, b'spam')
assert os.read(r2, 100) == b'spam'
os.write(w, b'eggs')
assert os.read(r2, 100) == b'eggs'
os.write(w, b'<DONE>')

t.join()
os.close(r)
os.close(w)
os.close(r2)
os.close(w2)


#############################

section_header('example 4')

"""
>>> r, w = os.pipe()
>>> def handler():
...     interp.run(f'''if True:
...         data = pickle.load( os.open({r}) )
...         handle_data(data)
...         ''')
...
>>> Thread(target=handler).start()
>>> pickle.dump('spam', os.open(w, 'w'))
"""

r, w = os.pipe()
r2, w2 = os.pipe()

def handler():
    interp.run(f'''if True:
        data = os.read({r}, 100)
        while data != b'<DONE>':
            data = pickle.loads(data)
            handle_data(data)
            os.write({w2}, data if isinstance(data, bytes) else data.encode('utf-8'))
            data = os.read({r}, 100)
        #with os.fdopen({r}, 'rb') as infile:
        #    data = pickle.load(infile)
        #    while data != b'<DONE>':
        #        os.write({w2}, data if isinstance(data, bytes) else data.encode('utf-8'))
        #        handle_data(data)
        #        data = pickle.load(infile)
        print('handler done!')
        ''')

t = Thread(target=handler)
t.start()

os.write(w, pickle.dumps('spam'))
assert (v := os.read(r2, 100)) == b'spam', v
os.write(w, pickle.dumps('eggs'))
assert (v := os.read(r2, 100)) == b'eggs', v
os.write(w, b'<DONE>')
#with os.fdopen(w, 'wb') as outfile:
#    pickle.dump('spam', outfile)
#    assert os.read(r2, 100) == 'spam'
#    pickle.dump('eggs', outfile)
#    assert os.read(r2, 100) == 'eggs'
#    pickle.dump(b'<DONE>', outfile)

t.join()
os.close(r2)
os.close(w2)


#############################

section_header('example 5')

"""
>>> rch, sch = channels.create()
>>> def handler():
...     interp.run('''if True:
...         while True:
...             handle_data( rch.recv() )
...         ''', channels={'rch': rch})
...
>>> Thread(target=handler).start()
>>> sch.send(b'spam')
"""

#rch, sch = interpreters.create_channel()
#
#def handler():
#    interp.run('''if True:
#        data = rch.recv()
#        while data:
#            handle_data(data)
#            data = rch.recv()
#        ''', channels={'rch': rch})
#
#t = Thread(target=handler)
#t.start()
#
#sch.send(b'spam')
#sch.send(b'eggs')
#sch.send(b'')
#
#t.join()


#############################

section_header('example 6')

"""
>>> rch, sch = channels.create()
>>> def handler():
...     interp.run('''if True:
...         handle_data( rch.recv() )
...         ''', shared={'rch': rch})
...
>>> Thread(target=handler).start()
>>> data = np.array([1, 2, 3])
>>> sch.send(data)
"""

#rch, sch = interpreters.create_channel()
#
#def handler():
#    interp.run('''if True:
#        handle_data( rch.recv() )
#        ''', shared={'rch': rch})
#
#Thread(target=handler).start()
#data = np.array([1, 2, 3])
#sch.send(data)
