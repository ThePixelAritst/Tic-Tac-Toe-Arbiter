#import Engine_handler
import Resources.program_settings as set
import os




class Engine_instance_managment:
    def __init__(self): #makes a list of all avaliable engines
        os.chdir(r"D:\Coding adventures\Tic Tac Arbiter\Engines") #set this to set.Engine_folder when you are done with testing
        
        self.engine_list = []
        self._calculate_engine_list()

    def _calculate_engine_list(self):
        Folder_scan = os.scandir()
        for engine in Folder_scan:
                    if engine.is_dir() and "engine" in engine.name.casefold():
                        self.engine_list.append(engine.path)

    def get_engine_path(self,engine_id):
        if engine_id >= len(self.engine_list):
            return None
        else:
            return self.engine_list[engine_id]


"""if __name__ == "__main__":
    Engine_1 = Engine_handler.Engine_handler(NotImplemented,1)
    print("stink")
    Engine_1 = Engine_handler.Engine_handler(NotImplemented,2)

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
"""