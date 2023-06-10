import _xxsubinterpreters as interpreters

from threading import Thread

import textwrap as tw



def test_threading_interpreter():
    interp = interpreters.create()

    def t():
        interpreters.run_string(interp,tw.dedent("""
            import time
            for _ in range(50):
                print(end='.', flush=True)
                time.sleep(0.05)
            print("End of interp job")
        """))

    thread = Thread(target = t)
    print(f"Before thread.start(), {interpreters.is_running(interp) = }")
    thread.start()
    print(f"After thread.start(), {interpreters.is_running(interp) = }")
    thread.join()
    print(f"After thread.join(), {interpreters.is_running(interp) = }")


if __name__ == "__main__":
    test_threading_interpreter()
