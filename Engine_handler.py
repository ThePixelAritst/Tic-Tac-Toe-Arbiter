from multiprocessing import Process
import multiprocessing.connection as mpcon
import hashlib
import psutil

class Engine_handler:
    def __init__(self,engine,engine_identificator,cpu_affinity,max_memory):
        self.identificator = engine_identificator
        self.arbiter_conn, self.engine_conn = mpcon.Pipe()
        self.engine = Process(target=engine,args=(self.engine_conn))
        self.engine.start()
        self.process = psutil.Process(self.engine.pid)

        try:
            self._communication_handshake()
        except RuntimeError:
            pass

        

    def _communication_handshake(self):
        retry_counter = 0
        while True:
            if self._receive_data(2) is ("INITIAL","start"):
                break
            elif retry_counter > 5:
                raise RuntimeError("Connection to engine could not be established")
            retry_counter += 1


        

        

    def _define_dictionaries(self):
        self.handshake_dict = {}
            
        



    def _receive_data(self,watchdog=2.5):
        received = mpcon.wait([self.arbiter_conn],watchdog)
        if self.arbiter_conn in received:
            return self.arbiter_conn.recv()
        else: return None

    def move(self,*arguments):
        self.arbiter_conn.send(("move",arguments))
        return self._receive_data()

    def _close(self):
        self.arbiter_conn.send(type(None))
        self.engine.join()
        print(f"Engine {self.identificator} process closed successfully")

    def _terminate(self):
        self.engine.terminate()
        print(f"Engine {self.identificator} process forcefully terminated")