from multiprocessing import Process
import multiprocessing.connection as mpcon
import hashlib
import psutil

class Engine_handler:
    def __init__(self,engine_folder_path, engine_identificator, cpu_affinity:tuple, max_memory:int):
        self.identificator = engine_identificator

        if self._verify_comms_file():
            self.engine.start()
        else:
            raise ImportError("Incorrect or tampered communications file")

        self.arbiter_conn, self.engine_conn = mpcon.Pipe()
        self.engine = Process(target=engine_folder_path,args=(self.engine_conn))
        self.process = psutil.Process(self.engine.pid)
        self.process.cpu_affinity(cpu_affinity)
        self.process.memory_percent()



    def _verify_comms_file():
        pass

        

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