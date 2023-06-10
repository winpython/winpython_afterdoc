# runs on IDLE

from collections import namedtuple
import subprocess
import time
import _xxsubinterpreters as interpreters
import unittest
#internam from test import interpreters


def iter_counter(maxi=1000):
    for i in range(1, maxi+1):
        text = '.'
        if i % 100 == 0:
            text += '\n'
        elif i % 20 == 0:
            text += '   '
        elif i % 5 == 0:
            text += ' '
        if i % 1000 == 0:
            text += f'<{i}>\n'
        if i % 500 == 0:
            text += '\n'
        yield i, text


#class MemoryUsage(namedtuple('MemoryUsage', 'kind total used free')):
#
#    KINDS = ['mem', 'swap']
#    COLUMNS = 'total used free shared buff/cache available'.split()
#
#    _extra = None
#
#    @classmethod
#    def from_host(self):
#        proc = subprocess.run('free', shell=True, capture_output=True, text=True)
#        if proc.returncode != 0:
#            return None, None
#        line1, line2, line3 = proc.stdout.splitlines()
#        assert line1.split() == cls.COLUMNS, repr(proc.stdout)
#        mem = cls.parse(line2)
#        swap = cls.parse(line3)
#        return mem, swap
#
#    @classmethod
#    def parse(cls, line):
#        values = line.split()
#        data = [int(v) for v in values[1:]]
#        if values[0] == 'Mem:':
#            kind = 'mem'
#            extra = data[3:]
#            assert len(extra) == 3, repr(line)
#        elif values[0] == 'Swap:':
#            kind = 'swap'
#            extra = None
#        else:
#            raise NotImplementedError(repr(line))
#        self = cls(kind, *data[:3])
#        self._extra = extra
#        return self
#
#    @property
#    def shared(self):
#        if self._extra is None:
#            return None
#        return self._extra[0]
#
#    @property
#    def buff_cache(self):
#        if self._extra is None:
#            return None
#        return self._extra[1]
#
#    @property
#    def available(self):
#        if self._extra is None:
#            return None
#        return self._extra[2]


def get_memory_usage():
    #return MemoryUsage.from_host()[0].used
    proc = subprocess.run('free', shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    cols = 'total used free shared buff/cache available'.split()
    line1, line2, line3 = proc.stdout.splitlines()
    assert line1.split() == cols, repr(proc.stdout)
    assert line2.startswith('Mem:')
    _, total, used, free, *_ = line2.split()
    return int(used)


def create_interpreters(maxnum=1000):
    mem_before = get_memory_usage()

    # Create the interpreters, one at a time.
    print(f'creating {maxnum} interpreters...')
    total_create_time = 0
    cached = []
    for i, text in iter_counter(maxnum):
        print(text, end='', flush=True)
        start = time.time()
        interp = interpreters.create()
        end = time.time()
        total_create_time += end - start
        # Keep a reference.
        cached.append(interp)
    if i % 100 != 0:
        print()
    print()

    mem_after = get_memory_usage()

    # Destroy them, one at a time.
    print(f'destroying {maxnum} interpreters...')
    total_destroy_time = 0
    while cached:
        interp = cached.pop()
        start = time.time()
        #interp.destroy()
        #interp.destroy()
        #pfg interpreters.destroy(interp.id)
        interpreters.destroy(interp)
        end = time.time()
        total_destroy_time += end - start
    print()

    # Show the results:
    create_time = total_create_time / maxnum
    destroy_time = total_destroy_time / maxnum
    if mem_before and mem_after:
        mem_used = (mem_after - mem_before) / maxnum
        if mem_used >= 1000:
            mem_used = f'{mem_used/1000:,.2f} MB'
        elif mem_used >= 100:
            mem_used = f'{int(mem_used)} kB'
        else:
            mem_used = f'{mem_used:,.2f} kB'
    else:
        mem_used = ' ???'
    print('##### results ######')
    print(f'# interpreters:    {maxnum}')
    print(f'avg. create time:  {create_time:.3f} s')
    print(f'avg. destroy time: {destroy_time:.3f} s')
    print(f'avg. memory used:  {mem_used}')



if __name__ == '__main__':
    import sys
    maxarg = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    create_interpreters(maxarg)
