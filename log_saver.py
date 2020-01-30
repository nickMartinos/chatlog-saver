import subprocess
import time
import psutil
import shutil
from shutil import copyfile
import os
from datetime import datetime
from pathlib import Path

global _running, previously_running, _path_

_cfg_name = "settings.cfg"


def save_log():

    now = datetime.now()
 
    dt_string = now.strftime("%d-%m-%Y %H;%M;%S")

    # Source path 
    src = _path_ + "\chatlog.txt"

    # Destination path
    curr_path = str(Path(__file__).resolve().parent)
    dest = curr_path + "\chatlog {}.txt".format(dt_string)
      
    # Copy the content of 
    # source to destination 
    shutil.copy(src, dest)

    
def create_file():
    try:
        f = open(_cfg_name)
        # Do something with the file
    except IOError:
        f = open(_cfg_name, "x")
        print("File not accessible, created.")
    finally:
        f.close()
    

def set_up():
    
    global _path_
    _path_ = ""
    create_file()
    config = open(_cfg_name, "r")
    _path_ = config.read()

    while True:
        if _path_ is None or _path_ == "":
            _path_ = input("Where are your SA:MP chatlogs stored?: ")
            inp = input("Is {} your directory? (Y/n): ".format(_path_))
            if inp == "Y" or inp == "y":
                break
            elif inp == "N" or inp == "n":
                _path_ = ""
                print("Resetting")
            else:
                _path_ = ""
                print("Wrong input; either y/Y for yes, or n/N for no.")
        else:
            inp = input("Saved path: '{}' || Is this correct (y/N)?: ".format(_path_))
            if inp == "Y" or inp == "y":
                break
            elif inp == "N" or inp == "n":
                _path_ = ""
                print("Resetting")
            else:
                print("Wrong input; either y/Y for yes, or n/N for no.")

    config.close()
    config = open(_cfg_name, "w")
    lines = []
    lines.append(_path_)
    config.writelines(lines)
    config.close()

    
def process_exists(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


def start_up():
    global _running, previously_running
    if process_exists('gta_sa'):
        previously_running = True
        _running = True
        print("Running GTA_SA instance detected.")
    else:
        previously_running = False
        _running = False
        print("Running GTA_SA instance not detected.")
    process_running_loop()
    

def process_running_loop():
    global _running, previously_running
    while True:
        if process_exists('gta_sa'):
            _running = True
            previously_running = True
            print("GTA Sa currently running")
        elif not process_exists('gta_sa'):
            _running = False
            
        if not _running and previously_running:
            previously_running = False
            print("Logged outs, saving logs.")
            save_log()
        time.sleep(5)

set_up()
start_up()
