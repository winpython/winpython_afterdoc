# this one works when launched from IDLE
import _xxsubinterpreters as interpreters
#from test import interpreters
from threading import Thread
from textwrap import dedent

from textwrap import dedent
import os
# https://github.com/python/cpython/blob/
#   15665d896bae9c3d8b60bd7210ac1b7dc533b093/Lib/test/test__xxsubinterpreters.py#L75
def _captured_script(script):
    r, w = os.pipe()
    indented = script.replace('\n', '\n                ')
    wrapped = dedent(f"""
        import contextlib
        with open({w}, 'w', encoding="utf-8") as spipe:
            with contextlib.redirect_stdout(spipe):
                {indented}
        """)
    return wrapped, open(r, encoding="utf-8")


def _run_output(interp, request, channels=None):
    script, rpipe = _captured_script(request)
    with rpipe:
        interpreters.run_string(interp,script, shared=channels)
        return rpipe.read()
    
main = interpreters.get_main()
print(f"Main interpreter ID: {main}")
# Main interpreter ID: Interpreter(id=0, isolated=None)

interp = interpreters.create()

print(f"Sub-interpreter: {interp}")
# Sub-interpreter: Interpreter(id=1, isolated=True)

# https://github.com/python/cpython/blob/
#   15665d896bae9c3d8b60bd7210ac1b7dc533b093/Lib/test/test__xxsubinterpreters.py#L236
code = dedent("""
            #from test.support import interpreters
            import _xxsubinterpreters as interpreters
            cur = interpreters.get_current()
            print(cur)
            """)

out = _run_output(interp, code)

print(f"All Interpreters: {interpreters.list_all()}")
# All Interpreters: [Interpreter(id=0, isolated=None), Interpreter(id=1, isolated=None)]
print(f"Output: {out}")  # Result of 'print(cur.id)'
# Output: 1
