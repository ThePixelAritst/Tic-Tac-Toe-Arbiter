from multiprocessing import Process as mppr
import multiprocessing.connection as mpcon

class Arbiter_communication:
    # IMPORTANT NOTE: YOUR ENGINE WILL NOT EVEN START IF YOU TOUCH ANYTHING IN HERE!

    # Public-facing functions, which you can (and need) to use in order to communicate with the Arbiter

    def receive_arbiter_instruction(self):
        request = self.pipe.recv() # blocking instruction - waits for data from Arbiter
        if self._check_receive_validity(request):
            return request
        else:
            raise ValueError("Invalid request received, resending")
            

    def send_to_arbiter(self,data_to_send): #sends the inputed data packet to Arbiter through pipe
        if not data_to_send:
            raise ValueError("Empty packet cannot be sent to Arbiter!")
        self.pipe.send(data_to_send)

    # Interal back-end functions and workings, you likely wont need these :D

    def __init__(self,pipe_conn: mpcon.Connection):
            self.done_handshake = False
            self.pipe = pipe_conn
            self._define_translation_dictionary()     
            self.send_to_arbiter(("INITIAL","READY"))

    def _handshake(self):
        while not self.done_handshake:
            instruction = self.receive_arbiter_instruction()


    def _define_translation_dictionary(self):
        self.arbiter_translation = {
            "HANDSHAKE":(self._handshake(),0)
            }
        
        self.translate_receive_type = {
            "MOVE": int,
            "PONDER" : int,
            "SETTINGS" : int,
            }


    def _check_receive_validity(self,input_data):
        if input_data is type(None):
            self.send_to_arbiter(("ARBITER","PIPE_CLOSED"))
            self.pipe.close()

        if not self.done_handshake:
            return True
        elif input_data[0] is "ARBITER":
            argument_length = len(input_data)-2
            requested_function = self.arbiter_translation.get(input_data[1],KeyError)
        else:
            requested_function = self.translate_receive_type.get(input_data[0],KeyError)
            argument_length = len(input_data)-1

        if requested_function is not KeyError and argument_length == requested_function[1]:
            return True
        else:
            self.send_to_arbiter(("ARBITER","INVALID_REQUEST",input_data))
            return False







class Engine_handler:
    def __init__(self,engine,engine_numerator):
        self.identificator = engine_numerator
        self.arbiter_conn, self.engine_conn = mpcon.Pipe()
        self.eng = mppr(target=engine,args=(self.engine_conn))
        self.eng.start()
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
        self.eng.join()
        print(f"Engine {self.identificator} process closed successfully")

    def _terminate(self):
        self.eng.terminate()
        print(f"Engine {self.identificator} process forcefully terminated")



if __name__ == "__main__":
    engine_1 = Engine_handler(Arbiter_communication,1)
    engine_1._close()