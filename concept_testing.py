import multiprocessing as mp
from multiprocessing.connection import wait
import time
import os

def engine_worker(conn):
    # This function's code runs in a *separate* process, not the parent.
    # `conn` is this process's end of the pipe — its "phone line" to the parent.
    while True:
        msg = conn.recv()               # blocks until the parent sends something
        if msg is None:                 # a simple convention: None = shut down
            break
        time.sleep(1)                   # pretend this is "thinking" about a move
        conn.send(("move", 4, -1))      # send the result back down the same pipe

if __name__ == "__main__":
    parent_conn, child_conn = mp.Pipe()
    # Pipe() gives you TWO connected endpoints — think two ends of a phone line.
    # Whatever one end sends, the other end can recv.

    p = mp.Process(target=engine_worker, args=(child_conn,))
    # This doesn't run anything yet — it just prepares a new process
    # that will call engine_worker(child_conn) once started.
    # We hand it child_conn (not parent_conn) — that's the engine's phone.
    print(os.process_cpu_count())
    p.start()
    # NOW the OS actually spawns the new process. engine_worker starts
    # executing there, immediately blocking on conn.recv().

    parent_conn.send(("go", "board_state_here"))
    # We use OUR end (parent_conn) to send the request. This arrives
    # on the other side as the value engine_worker's conn.recv() returns.

    ready = wait([parent_conn], timeout=5)
    # Block here until parent_conn has data waiting, or 5 seconds pass.
    # `ready` is a list: either [parent_conn] (something arrived) or [] (timeout).

    if parent_conn in ready:
        result = parent_conn.recv()     # actually pull the message out
        print("Got:", result)
        parent_conn.send(None)
    else:
        print("Timed out — killing process")
        p.terminate()                   # forcibly ends the child process

    p.join()
    
    # Waits for the process to actually finish exiting before moving on —
    # cleans up OS-level resources (like a subprocess-flavored thread.join()).