from multiprocessing import Process
import multiprocessing.connection as mpcon
import hashlib
import psutil
import os

import Resources.program_settings as set

class Data_receive:
    pass

class Engine_handler(Data_receive):
    def __init__(self,engine_folder_path, engine_identificator, cpu_affinity:tuple):
        self.identificator = engine_identificator

        if self._verify_comms_file():
            self.engine.start()
            pass
        else:
            raise ImportError("Incorrect or tampered communications file")

        self.arbiter_conn, self.engine_conn = mpcon.Pipe()
        self.engine = Process(target=engine_folder_path,args=(self.engine_conn))
        self.process = psutil.Process(self.engine.pid)
        self.process.cpu_affinity(cpu_affinity)



    def _verify_comms_file(self):
        comms_address = os.path.join(set.Engine_folder,"Arbiter_communications.py")
        print("stink")
        if os.path.exists(comms_address) and os.path.isfile(comms_address):
            with open(comms_address, "rb") as engine_file:
                digested_engine_file = hashlib.file_digest(engine_file, "sha256")
                digested_engine = digested_engine_file.hexdigest()
            with open(r"C:\Users\pixel\Documents\Coding\Tic-Tac-Arbiter\Engine_base\Arbiter_communications.py", "rb") as engine_file:
                digested_arbiter = hashlib.file_digest(engine_file, "sha256")
                digested_arbiter = digested_engine_file.hexdigest()

            if digested_arbiter == digested_engine:
                return True
        else:
            return False


        

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
