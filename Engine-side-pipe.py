from multiprocessing import Process as mppr
import multiprocessing.connection as mpcon


# VERSION --- V1.0.0

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
            self.done_handshake = False
            self.pipe = pipe_conn
            self.pipe_open = True
            self._define_translation_dictionary()
            self.send_to_arbiter(("ARBITER","READY",()))
            

    def _handshake(self):
        if not self.receive_arbiter_instruction():
            print("Engine has failed communication handshake")
            self.send_to_arbiter(("ARBITER","FATAL",()))
            return

        while not self.done_handshake:
            request, valid = self.receive_arbiter_instruction()
            if valid:
                self.send_to_arbiter(("ARBITER","FUNCTION-VALID",(request)))
            else:
                self.send_to_arbiter(("ARBITER","fUNCTION-INVALID",(request)))
                

    def _define_translation_dictionary(self):
        self.arbiter_translation = {
            "HANDSHAKE_START":(self._handshake,0),
            "PIPE_CLOSE": (self.__close_pipe,0),
            "HANDSHAKE_OK" : (self.__confirm_handshape,0)
            }
        
        self.translate_public_function = {
            "MOVE": int,
            "PONDER" : int,
            "SETTINGS" : int
            }


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
        elif valid and self.done_handshake:
            return received_data 
        elif not self.done_handshake:
            return received_data, valid
        else:
            raise ValueError("Invalid request received")


    def __confirm_handshape(self):
        self.done_handshake = True


    def __close_pipe(self):
        self.send_to_arbiter(("ARBITER","PIPE_CLOSED",()))
        self.pipe.close()


        






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