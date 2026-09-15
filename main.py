from multiprocessing import Process as mppr
import multiprocessing.connection as mpcon
import time
import random


class Engine_Imitator:
    def __init__(self, engine_number,pipe_conn):
        self.pipe = pipe_conn
        translate = {"move":self.turn_call}
        print(f"Engine {engine_number} initiated")

        while True:
            request = self.pipe.recv()
            if request is None:
                break
            elif translate.get(request[0]) is not None:
                return translate.get(request[0])(request[1])
            else: raise KeyError("Requested function does not exist")

    def turn_call(self,*args):
        random_timer = random.randrange(1,4)
        print(f"generated_timer: {random_timer}")
        time.sleep(random_timer)
        move = tuple((random.randint(1,10),random.randint(1,10)))
        print(move)
        self.pipe.send(move)

class Engine_handler:
    def __init__(self,engine,engine_numerator):
        self.identificator = engine_numerator
        self.arbiter_conn, self.engine_conn = mpcon.Pipe()
        self.eng = mppr(target=engine,args=(engine_numerator,self.engine_conn))
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
        self.arbiter_conn.send(None)
        self.eng.join()
        print(f"Engine {self.identificator} process closed successfully")

    def _terminate(self):
        self.eng.terminate()



if __name__ == "__main__":
    Engine_1 = Engine_handler(Engine_Imitator,1)
    print("stink")
    Engine_2 = Engine_handler(Engine_Imitator,2)

    print("sending test move")
    test_move = Engine_1.move()
    print(f"received test move, data {test_move}")
    if not test_move:
        print("Not valid")
        Engine_1._terminate()
        Engine_2._terminate()
    else: 
        Engine_1._close()
        Engine_2._close()
        print(test_move)
