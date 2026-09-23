import Arbiter_communications


class Main_Engine:
    def __init__(self,pipe_conn):
        self.comms = Arbiter_communications.Arbiter_communication(pipe_conn)

        self.translate = {
            "MOVE": self.check_move,
            "PONDER" : self.ponder
        }

    def main_loop(self):
        while True:
            request = self.comms.receive_arbiter_instruction()
            if not request:
                 continue
            instruction = self.translate.get(request[0])
            reply = instruction(request[1])
            self.comms.send_to_arbiter(request[0],reply)

            
    def check_move(self):
        NotImplemented

    def ponder(self):
        NotImplemented
