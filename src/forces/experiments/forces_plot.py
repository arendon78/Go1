import json
import matplotlib.pyplot as plt

import os 
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)


# json_path = '/forces/datas/forces.json'
# json_path = '/forces/datas/stop_each_2_steps_leaning_forward.json'
json_path = 'forces/datas/stop_each_4_step_leaning_forward.json'
# json_path = '/forces/datas/walking_50_points.json'
# json_path = '/forces/datas/walking_4_stops_50_points.json'


with open(os.path.join(project_root,json_path), 'r') as json_file:
    forces = json.load(json_file)


# Assuming time points are indices of the list
times = list(range(len(forces['FR'])))

# Extract forces for each limb
fr_forces = forces["FR"]
fl_forces = forces["FL"]
rr_forces = forces["RR"]
rl_forces = forces["RL"]

# Step 2: Plotting the data in subplots
fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

# Plotting each limb's forces
axs[0].plot(times, fr_forces, label='FR', marker='o')
# axs[0].plot(times, fl_forces, label='FL', marker='o')
axs[0].set_title('FR Forces Over Time')
axs[0].set_ylabel('Force')
axs[0].legend()

axs[1].plot(times, fl_forces, label='FL', marker='o')
axs[1].set_title('FL Forces Over Time')
axs[1].set_ylabel('Force')
axs[1].legend()

axs[2].plot(times, rr_forces, label='RR', marker='o')
axs[2].set_title('RR Forces Over Time')
axs[2].set_ylabel('Force')
axs[2].legend()

axs[3].plot(times, rl_forces, label='RL', marker='o')
axs[3].set_title('RL Forces Over Time')
axs[3].set_xlabel('Time')
axs[3].set_ylabel('Force')
axs[3].legend()

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
