#!/usr/bin/python
import os 
import sys
import json
import numpy as np

from utils import *
from unitree_legged_sdk.example_py.Bezier.foot_trajectory import *

from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron 
from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)


sys.path.append('../../lib/python/amd64')
# import robot_interface as sdk 

def compute_neurons(trajectories, controllers, watchers, V):
    """
    Computes the neuron activities, commands, and frequencies for a given set of trajectories.

    This function simulates the behavior of neural networks controlling a robot's limbs based on provided
    trajectories. The simulation runs for a specified simulation time and updates the neural activities,
    commands, and frequencies for each limb part.

    Parameters
    ----------
    trajectories : dict
        A dictionary containing the trajectory data for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of coordinates.
    
    controllers : dict
        A dictionary containing the controllers for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of three controllers for hip, thigh, and calf.
    
    watchers : dict
        A dictionary containing the watchers for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of three watchers for hip, thigh, and calf.
    
    V : dict
        A dictionary containing the voltage matrices used in the simulation. It is updated during the
        simulation to reflect the neural activities.

    Returns
    -------
    neurons_coords : dict
        A dictionary containing the coordinates of the neurons' activities for each part of the robot.
        The keys are 'FR', 'FL', 'RR', 'RL', and the values are lists of tuples (hip, thigh, calf) representing
        the frequency ratios of the respective neurons.
    
    command_coords : dict
        A dictionary containing the commanded positions for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of tuples (hip, thigh, calf) representing the target positions.
    
    frequency_parts : dict
        A dictionary containing the frequency ratios for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of frequency ratios for the hip, thigh, and calf neurons.
    
    command : dict
        A dictionary containing the commands sent to each part of the robot during the simulation.
        The keys are 'FR', 'FL', 'RR', 'RL', and the values are lists of commands for the hip, thigh, and calf.
    
    inside_oscillator : dict
        A dictionary containing the internal oscillator states for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of oscillator states for the hip, thigh, and calf.
    """

    SIM_TIME = 700
    N_STEPS = len(trajectories['FR'])
    parts = ['FR','FL','RR','RL']



    neurons_coords = {  'FR' : [],
                        'FL' : [],
                        'RR' : [],
                        'RL' : []
    }

    command_coords = {    'FR' : [],
                        'FL' : [],
                        'RR' : [],
                        'RL' : []

    }

    frequency_parts = { 'FR' : [[],[],[]]
    ,
                        'FL' : [[],[],[]]
                        ,
                        'RR' : [[],[],[]]
                        ,
                        'RL' : [[],[],[]]

    }

    command         = { 'FR' : [[],[],[]]
    ,
                        'FL' : [[],[],[]]
                        ,
                        'RR' : [[],[],[]]
                        ,
                        'RL' : [[],[],[]]

    }

    inside_oscillator = { 'FR' : [[],[],[]]
    ,
                        'FL' : [[],[],[]]
                        ,
                        'RR' : [[],[],[]]
                        ,
                        'RL' : [[],[],[]]

    }


    for part in parts : 
        for n in range(0,3):
            controllers[part][n].update_adjacency_matrix()
            # print(controllers[part][n].adjacency.size)
            # controllers[part][n].print_network('controller')


    # data_json = {
    #     part : {
    #         n : (controllers[part][n].adjacency, [np.zeros([(SIM_TIME * N_STEPS),1]) for _ in range (controllers[part][n].adjacency.size) ])
    #     for n in [0,1,2]
    #     }
    #     for part in parts
    # }

    # data_json = {
    #     part : {
    #         n : [controllers[part][n].adjacency, [[np.zeros([(SIM_TIME),2]) for _ in range (controllers[part][n].adjacency.size)] for __ in range(N_STEPS) ], [1 if isinstance(neuron,Excitatory_Neuron) else 0 for neuron in controllers[part][n].brain] ]
    #     for n in [0,1,2]
    #     }
    #     for part in parts
    # }

    data_json = {
        part : {
            n : [controllers[part][n].adjacency, [np.zeros([(SIM_TIME*N_STEPS),2]) for _ in range (controllers[part][n].adjacency.size)], [1 if isinstance(neuron,Excitatory_Neuron) else 0 for neuron in controllers[part][n].brain] ]
        for n in [0,1,2]
        }
        for part in parts
    }

    # print(data_json)


    print("\n\n -------- computation loop ---------- \n\n")


    #computation loop

    print(len(trajectories['FR']),"steps to simulate")
    for part in ['FR','FL','RR','RL']:
        
        internal_time = 0

        for i in range(len(trajectories['FR'])): 

            coords = {'FR': trajectories['FR'][i],
                'FL': trajectories['FL'][i],
                'RR': trajectories['RR'][i],
                'RL': trajectories['RL'][i]
            }


            print(i)
            # for part in parts : 

            
            
            # print(internal_time)
            x = coords[part][0]
            y = coords[part][1]
            z = 0

            hip = theta_hip(x,y,z)
            thigh = theta_thigh(x,y,z)
            calf = theta_calf(x,y,z)

            # #0
            inside_oscillator_hip = controllers[part][0].create_oscillators(hip)[0]
            # old version
            # controllers[part][0].pass_inputs(1)
            #new version 
            # print(data_json[part][0][1])
            if i == 0:
                controllers[part][0].pass_inputs(1)
            else : 
                controllers[part][0].pass_inputs(0)
            # print("first controller to be simualted")
            controllers[part][0].simulate(internal_time, data_json[part][0][1])
            # print(data_json[part][0][1][i])
            # print("size : ", np.size(data_json[part][0][1]))
            frequency_parts[part][0].append(watchers[part][0].frequency_ratio())

            #1
            inside_oscillator_thigh = controllers[part][1].create_oscillators(thigh)[0]
            # old version
            # controllers[part][1].pass_inputs(1)
            #new version
            if i == 0:
                controllers[part][1].pass_inputs(1)
            else : 
                controllers[part][1].pass_inputs(0)

            # print("2cd controller to be simualted")
            controllers[part][1].simulate(internal_time,data_json[part][1][1])
            frequency_parts[part][1].append(watchers[part][1].frequency_ratio())
           
            #2
            inside_oscillator_calf = controllers[part][2].create_oscillators(calf)[0]
            # old version
            # controllers[part][2].pass_inputs(1)
            #new version 
            if i == 0:
                controllers[part][2].pass_inputs(1)
            else : 
                controllers[part][2].pass_inputs(0)
            # print("third")
            controllers[part][2].simulate(internal_time,data_json[part][2][1])
            frequency_parts[part][2].append(watchers[part][2].frequency_ratio())
            

            internal_time+=1
            #simulate them for a reasonable time
            # problem : simulates all the neurons. should only simulate one neuron at a time (the one that is active)
            for j in range(SIM_TIME) : 
                # print("internal_time : ",internal_time)

                inside_oscillator[part][0].append(inside_oscillator_hip)
                inside_oscillator[part][1].append(inside_oscillator_thigh)
                inside_oscillator[part][2].append(inside_oscillator_calf)

                watchers[part][0].update_firing_rate(j)
                controllers[part][0].pass_inputs(0)
                None if j == 0 else controllers[part][0].simulate(internal_time,data_json[part][0][1])
                frequency_parts[part][0].append(watchers[part][0].frequency_ratio())
                command[part][0].append(hip)

                watchers[part][1].update_firing_rate(j)
                controllers[part][1].pass_inputs(0)
                None if j == 0 else  controllers[part][1].simulate(internal_time,data_json[part][1][1])
                frequency_parts[part][1].append(watchers[part][1].frequency_ratio())
                command[part][1].append(thigh)

                watchers[part][2].update_firing_rate(j)
                controllers[part][2].pass_inputs(0)
                None if j == 0 else controllers[part][2].simulate(internal_time,data_json[part][2][1])
                frequency_parts[part][2].append(watchers[part][2].frequency_ratio())
                command[part][2].append(calf)


                if j ==0 : 
                    None 
                else : 
                    internal_time +=1

            neuron_hip = watchers[part][0].frequency_ratio  ()
            neuron_thigh = watchers[part][1].frequency_ratio()
            neuron_calf  = watchers[part][2].frequency_ratio()
            
            #I don't care about neuron_hip in the first place

            neurons_coords[part].append((neuron_hip,neuron_thigh,neuron_calf))
            command_coords[part].append((hip,thigh,calf))
    # Display the neuron activities using matplotlib

    

    # saving the datas.

    for part in parts : 
        for n in range(3):
            for i in range(16): 
                data_json[part][n][1][i] = data_json[part][n][1][i].tolist()
                if i == 0: 
                    data_json[part][n][0] = data_json[part][n][0].matrix.tolist() 
                # data_json[part][n][0].pretty_print() 

                
    json_file_path = 'data/neuron_activity.json'

    with open(json_file_path, 'w') as json_file:
        json.dump(data_json, json_file)


# # Display the neuron activities using matplotlib in separate figures
#     for part in parts:
#         fig, axs = plt.subplots(1, 3, figsize=(15, 5))
#         fig.suptitle(f'Neuron Activities for Part: {part}')

#         for j, n in enumerate([0, 1, 2]):
#             adjacency, V = data_json[part][n]

#             # Create a list to store neuron activities across all steps for each neuron
#             neuron_activities = {neuron_idx: [] for neuron_idx in range(len(V[0]))}

#             for step in V:
#                 for neuron_idx, neuron_activity in enumerate(step):
#                     neuron_activities[neuron_idx].extend(neuron_activity.flatten())

#             for neuron_idx, activities in neuron_activities.items():
#                 axs[j].plot(activities, label=f'Neuron {neuron_idx}')

#             axs[j].set_title(f'Controller: {n}')
#             axs[j].legend()
#             axs[j].set_xlabel('Time Steps')
#             axs[j].set_ylabel('Activity')

#         plt.tight_layout(rect=[0, 0, 1, 0.96])
#         plt.show()

    print(data_json['FR'][1][2])

    return neurons_coords, command_coords, frequency_parts, command, inside_oscillator