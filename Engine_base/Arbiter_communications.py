import multiprocessing.connection as mpcon
import time

# VERSION --- V1.0.0
# API --- IAPI 1.0

class Arbiter_communication:
    # IMPORTANT NOTE: YOUR ENGINE WILL NOT EVEN START IF YOU TOUCH ANYTHING IN HERE!

    # Public-facing functions, which you can (and need) to use in order to communicate with the Arbiter

    def receive_arbiter_instruction(self):
        if not self.pipe_open:
            raise RuntimeError("Cannot receive data through closed pipe")
        request = self.pipe.recv() # blocking instruction - waits for data from Arbiter
        return self._handle_received(request)
            

    def send_to_arbiter(self,data_to_send): #sends the inputed data packet to Arbiter through pipe
        if not self.pipe_open:
            raise RuntimeError("Cannot send data through closed pipe")
        if not data_to_send:
            raise ValueError("Empty packet cannot be sent to Arbiter!")
        self.pipe.send(data_to_send)


    # Interal back-end functions and workings, you likely wont need these :D

    def __init__(self,pipe_conn: mpcon.Connection):
            self.pipe = pipe_conn
            self.pipe_open = True
            self._define_translation_dictionary()
            
            
    def _define_translation_dictionary(self):
        self.arbiter_translation = {
            "PIPE_CLOSE": (self.__close_pipe,0),
            "PING": (self._ping,1)
            }
        
        self.translate_public_function = {
            "MOVE": int,
            "PONDER" : int,
            "SETTINGS" : int
            }

    def _ping(self):
        self.send_to_arbiter(("ARBITER","PING_REPLY",(time.time_ns(),)))

    def _check_receive_validity(self,input_data):
        arbiter_method = False  
        if input_data[0] is "ARBITER":
            dictionary_reply = self.arbiter_translation.get(input_data[1],KeyError)
            if dictionary_reply is not KeyError:
                request_arguments = len(input_data[2])
                arbiter_method = True       
        else:
            dictionary_reply = self.translate_public_function.get(input_data[0],KeyError)
            if dictionary_reply is not KeyError:
                request_arguments = len(input_data[1])


        if requested_function is not KeyError:
            requested_function = dictionary_reply[0]
            function_arguments = dictionary_reply [1]
            if arbiter_method and type(requested_function) is not function:
                arbiter_method = False
            if request_arguments == function_arguments:
                return True, arbiter_method

        return False


    def _handle_received(self,received_data: tuple):
        valid, for_arbiter_execution = self._check_receive_validity()

        if for_arbiter_execution():
            self.arbiter_translation[received_data[1]](received_data[2])
        elif valid:
            return received_data 
        else:
            self.send_to_arbiter(("ARBITER","FUNCTION_INVALID",(received_data)))
            return None

    def __close_pipe(self):
        self.send_to_arbiter(("ARBITER","PIPE_CLOSED",()))
        self.pipe.close()