import sys
import os
sys.path.insert(0,str(os.getcwd()))

from Code.Engine_handler import Engine_handler
from Resources import program_settings





class Engine_instance_managment:
    def __init__(self): #makes a list of all avaliable engines
        current_folder = os.scandir()
        for item in current_folder:
            if item.name == "Engines":
                os.chdir(os.path.join(os.getcwd(),item.name))
                print(os.getcwd())
        
        self.engine_dict = {}
        self._calculate_engine_list()
        print(self.engine_dict)

    def _calculate_engine_list(self):
        _folder_scan = os.scandir()
        engine_id = 0
        for engine in _folder_scan:
            if engine.is_dir() and "engine" in engine.name.casefold():
                self.engine_dict.update({engine_id : (engine.name,engine.path)})
            engine_id += 1

    def get_data(self,engine_id:int):
        """
        Returned value: (engine_name,engine_path)
        """ 
        returned_value = self.engine_dict.get(engine_id,Exception)
        if returned_value == Exception:
            raise KeyError("Requested key does not exist")
        else:
            return returned_value

engines = Engine_instance_managment()

def engine_instance_start(engine_id):
    instance_data = engines.get_data(engine_id)
    return Engine_handler(os.path.join(os.getcwd(),instance_data[1]),instance_data[0],(0,1))

engine_instance_start(0)
engine_instance_start(1)

Engine_handler()
