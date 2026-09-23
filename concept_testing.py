import os
import Resources.program_settings as set

os.chdir(r"D:\Coding adventures\Tic Tac Arbiter\Engines")
Folder_scan = os.scandir()
Engine_list = []
for engine in Folder_scan:
    if engine.is_dir() and "Engine" in engine.name:
        print(f"Engine {engine.name} is avaliable")
        Engine_list.append(engine.path)

print(Engine_list)