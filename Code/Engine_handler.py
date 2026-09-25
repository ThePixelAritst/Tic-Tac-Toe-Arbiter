from multiprocessing import Process
import multiprocessing.connection as mpcon
import hashlib
import psutil
import os

import Resources.program_settings as set

class Data_receive:
    pass

class Engine_handler(Data_receive):
    def __init__(self,engine_directory, engine_identificator, cpu_affinity:tuple):
        self.identificator = engine_identificator

        if not os.path.isdir(self.path): # checks if provided engine directory exists
            raise ValueError("The engine directory could not be found")
        try: self._verify_comms_file()
        except Exception as error: raise error 
        self.path = engine_directory
        self.path_main_file = os.path.join(self.path,"Engine_main.py") #path of the script which will be launched
        if not os.path.isfile(self.path_main_file): #checks if the path is valid and a file
            raise ImportError(f"{set.ENGINE_MAINFILE} file does not exist or could not be found")

        self.arbiter_conn, self.engine_conn = mpcon.Pipe()
        self.engine = Process(target=self.path_main_file,args=(self.engine_conn))
        self.process = psutil.Process(self.engine.pid)
        self.process.cpu_affinity(cpu_affinity)

    def _verify_comms_file(self):
        comms_address = os.path.join(self.path,set.COMMS_FILENAME)
        if os.path.isfile(comms_address):
            with open(comms_address, "rb") as engine_file:
                digested_engine_file = hashlib.file_digest(engine_file, "sha256")
                digested_engine = digested_engine_file.hexdigest()
            with open(os.path.join(os.getcwd(),"Engine_base",set.COMMS_FILENAME), "rb") as engine_base_file:
                digested_arbiter = hashlib.file_digest(engine_base_file, "sha256")
                digested_arbiter = digested_engine_file.hexdigest()

            if digested_arbiter == digested_engine:
                engine_file.close()
                engine_base_file.close()
                return True
            else:
                raise ImportError(f"Verification {set.COMMS_FILENAME} file does not match with one found in Engine folder")
        else:
            raise FileNotFoundError(f"{set.COMMS_FILENAME} does not exist or could not be found")

    def start_resume_engine(self):


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
