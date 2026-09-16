from multiprocessing import Process as mppr
import multiprocessing.connection as mpcon
import time

class Arbiter_communication:

    def main_loop(self): # main loop in which the actual engine classes and functions are called
        pass


    def receive_arbiter_instruction(self):
        request = self.pipe.recv() # blocking instruction - waits for data from Arbiter
        print("Stink")
        if request is type(None): # signal to break the connection
            self.pipe.close()
        elif request is None:
            self.send_to_arbiter(())

    def send_to_arbiter(self,data_to_send): #sends the inputed data packet to Arbiter through pipe
        if not data_to_send:
            raise ValueError("SEND ERROR: Cannot send empty packet to arbiter!")
        self.pipe.send(data_to_send)

    # Interal back-end functions and workings, you likely wont need these :D

    def __init__(self,pipe_conn):
            self.pipe = pipe_conn
            self._communication_dict_initiation()
            self.send_to_arbiter(("INITIAL","start"))

    def _arbiter_handshake(self):
        pass

    def _communication_dict_initiation(self):
        self.receive_type_translate = {
                    "FUNCTION": self.function_list,
                    "INITIAL" : self.handshake_functions
                    }
        self.handshake_functions = {}
        self.function_list = {}






class Engine_handler:
    def __init__(self,engine,engine_numerator):
        self.identificator = engine_numerator
        self.arbiter_conn, self.engine_conn = mpcon.Pipe()
        self.eng = mppr(target=engine,args=(self.engine_conn))
        self.eng.start()

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
        self.eng.join()
        print(f"Engine {self.identificator} process closed successfully")

    def _terminate(self):
        self.eng.terminate()



if __name__ == "__main__":
    engine_1 = Engine_handler(Arbiter_communication,1)
    engine_1._close()