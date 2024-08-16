import numpy as np
import json
import matplotlib.pyplot as plt
import random
import math
from utils_forces import *

json_path = './datas/forces.json'
# json_path = './datas/stop_each_2_steps_leaning_forward.json'
# json_path = './datas/stop_each_4_step_leaning_forward.json'
# json_path = './datas/walking_50_points.json'
# json_path = './datas/walking_4_stops_50_points.json'
with open(json_path, 'r') as json_file:
    forces = json.load(json_file)



times = list(range(len(forces['FR'])))

coordinates = {'FR':  [],
            'FL':  [],
            'RR':  [],
            'RL':  []
            }

parts =  ['FR','FL','RR', 'RL']

for i in range(0,len(times)-1) :
    for part in parts:
        p1 = (i,forces[part][i])
        p2 = (i+1,forces[part][i+1])
        d = calculate_derivative(p1,p2)
        coordinates[part].append([p1[0],p1[1],d])


for part in parts: 
    coordinates[part].append([len(times)-1,0,0])


fr_coordinates = coordinates["FR"]#[:len(coordinates['FR'])//2]
fl_coordinates = coordinates["FL"]
rr_coordinates = coordinates["RR"]
rl_coordinates = coordinates["RL"]

times = times = list(range(len(fr_coordinates)))

#-------------- to decomment once finished
local_maxes = monte_carlo_gradient(1,fr_coordinates)

#---------------- to decomment once finished

local_mins = monte_carlo_gradient(-1,fr_coordinates)

# ------------------

#builds an ordered list (along time axis) of maxes and mins 

merged_mins_maxes_coordinates = build_merge(local_maxes, local_mins)
print(merged_mins_maxes_coordinates)



#finding cuvre pattern


find_pattern(merged_mins_maxes_coordinates,fr_coordinates)



#plotting from the merged datas to make sure it is good


def filter_max(el) : 
    return el[3] == "max"

def filter_min(el) :
    return el[3] == "min"


local_maxes = []
local_maxes = filter(filter_max,merged_mins_maxes_coordinates)
local_maxes = [[el[0],el[1],el[2]] for el in local_maxes]

filled_fr_maxes = [[i,0,0] for i in range(len(times))]
fr_list_indices_times_maxes = [local_maxes[i][0] for i in range(len(local_maxes)) ]
for t in fr_list_indices_times_maxes : 
    filled_fr_maxes[t] = find_value( t, local_maxes )

local_mins = []
local_mins = filter(filter_min,merged_mins_maxes_coordinates)
local_mins = [[el[0],el[1],el[2]] for el in local_mins]

filled_fr_mins = [[i,0,0] for i in range(len(times))]
fr_list_indices_times_mins = [local_mins[i][0] for i in range(len(local_mins)) ]
for t in fr_list_indices_times_mins : 
    filled_fr_mins[t] = find_value(t, local_mins)



# Step 2: Plotting the data in subplots
fig, axs = plt.subplots(4, 1, figsize=(10, 20), sharex=True)

# Plotting each limb's forces
# axs[0].plot(times, fr_forces, label='FR', marker='o')
axs[0].plot(times, [fr_coordinates[i][1] for i in range (len(fr_coordinates))], label='FR', marker='o')
axs[0].plot(times, [filled_fr_maxes[i][1] for i in range(len(filled_fr_maxes))], label='FR maxes', marker='o')
axs[0].plot(times, [filled_fr_mins[i][1] for i in range(len(filled_fr_mins))], label='FR mins', marker='o')
axs[0].set_title('FR Forces Over Time')
axs[0].set_ylabel('Force')
axs[0].legend()

# axs[1].plot(times, fl_forces, label='FL', marker='o')
axs[1].plot(times, [fl_coordinates[i][1] for i in range (len(fl_coordinates))], label='FL', marker='o')
axs[1].set_title('FL Forces Over Time')
axs[1].set_ylabel('Force')
axs[1].legend()

# axs[2].plot(times, rr_forces, label='RR', marker='o')
axs[2].plot(times, [rr_coordinates[i][1] for i in range (len(rr_coordinates))], label='FL', marker='o')
axs[2].set_title('RR Forces Over Time')
axs[2].set_ylabel('Force')
axs[2].legend()

# axs[3].plot(times, rl_forces, label='RL', marker='o')
axs[3].plot(times, [rl_coordinates[i][1] for i in range (len(rl_coordinates))], label='FL', marker='o')
axs[3].set_title('RL Forces Over Time')
axs[3].set_xlabel('Time')
axs[3].set_ylabel('Force')
axs[3].legend()

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
