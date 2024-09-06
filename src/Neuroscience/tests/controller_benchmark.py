import numpy as np
import matplotlib.pyplot as plt
import time

import os 
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Frequency_Detector import Frequency_Detector

res = 0.1

def find_combinations(controller) : 
    NUM = 1000

    for i in range(NUM)  :
        controller.create_oscillators(i/NUM)



# also counting instanciation time
start_old = time.time()

ctrl_old = Controller(res,use_old_combinations=True)
ctrl_old.create_oscillators(0)
find_combinations(ctrl_old)

end_old =time.time()



start_new = time.time()

ctrl_new = Controller(res,use_old_combinations=False)
ctrl_new.create_oscillators(0)
find_combinations(ctrl_new)

end_new =time.time()


new_time = end_new - start_new
old_time = end_old - start_old
print("deprecated because controllers are sharing the same main list now")
print("Benchmark ! \n New controller time : ", new_time, "\n Old controller time : ", old_time, " \nWhat a win for the new controller !! ")
print("That's ",  old_time/new_time," times faster !!")

print("But... Are they commanding the exact same thing ? ")

def compare_commands(ctrl1,ctrl2): 
    NUM = 1000
    for i in range(NUM):
        assert ctrl1.create_oscillators(i/NUM)[0] == ctrl2.create_oscillators(i/NUM)[0]

compare_commands(ctrl_new,ctrl_old)
print("comparison test is a success !")
