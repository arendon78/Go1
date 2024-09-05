import os 
import sys
import time
import math
import json
import time 

from utils import *
from unitree_legged_sdk.example_py.Bezier.stand_up_procedure import * 
from unitree_legged_sdk.example_py.Bezier.lie_down_procedure import * 
from unitree_legged_sdk.example_py.Bezier.foot_trajectory import *
from unitree_legged_sdk.example_py.Bezier.computation_neuron import *
from unitree_legged_sdk.example_py.Bezier.error_calculation import *
from unitree_legged_sdk.example_py.Bezier.plot_neurons import *
from unitree_legged_sdk.example_py.Bezier.main_loop import *
from forces.utils_forces import *
from unitree_legged_sdk.example_py.Bezier.Foot_Sensor import Foot_Sensor
from unitree_legged_sdk.example_py.Bezier.Behavior_Walking_2_bits import Behavior_Walking_2_bits


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)


from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Frequency_Detector import Frequency_Detector


sys.path.append('../../lib/python/amd64')
# import robot_interface as sdk
import robot_interface as sdk






def main_loop_v2(trajectories,trajectory,TOTAL_OFFSET,neurons_coords,parts,stand_up_1):
    """
    The main control loop for managing the robot's movement, including standing up, walking, and lying down.

    Parameters
    ----------
    trajectories : dict
        A dictionary containing the movement trajectories for each limb (FR, FL, RR, RL).
    
    trajectory : list
        A list of control points used to generate the foot trajectory.
    
    TOTAL_OFFSET : int
        The total offset applied to the trajectories for phase-shifting limb movements.
    
    neurons_coords : dict
        Precomputed neuron coordinates used to simulate the robot's movement.
    
    parts : list of str
        A list of parts (limbs) being controlled, including 'FR' (Front Right), 'FL' (Front Left), 'RR' (Rear Right), and 'RL' (Rear Left).
    
    stand_up_1, stand_up_2, stand_up_3 : dict
        Dictionaries containing the joint angle trajectories for the robot's standing up procedure.
    """

    json_path = './data/forces_copy.json'# mock data
    with open(json_path, 'r') as json_file:# mock data
        mock_forces = json.load(json_file)# mock data
    
    d = {'FR_0':0, 'FR_1':1, 'FR_2':2,
         'FL_0':3, 'FL_1':4, 'FL_2':5, 
         'RR_0':6, 'RR_1':7, 'RR_2':8, 
         'RL_0':9, 'RL_1':10, 'RL_2':11 }
    

    PosStopF  = math.pow(10,9)
    VelStopF  = 16000.0

    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff

    dt = 0.002  

    qInit = {parts[i] : [0,0,0] for i in range(len(parts))}
    
    qDes = {parts[i] : [0,0,0] for i in range(len(parts))}

    rate_count = 0

    udp = sdk.UDP(LOWLEVEL, 8080, "192.168.123.10", 8007)
    safe = sdk.Safety(sdk.LeggedType.Go1)
    
    cmd = sdk.LowCmd()
    state = sdk.LowState()
    udp.InitCmdData(cmd)

    Tpi = 0
    motiontime = 0

    forces = { 'FR' : [],
               'FL' : [],
               'RR' : [],
               'RL' : [],
    }

    old_frame = []
    foot_sensor = Foot_Sensor()
    is_step = False
    behavior_walking = Behavior_Walking_2_bits(neurons_coords)#I give it the whole movements of the different limbs.
    p=0


    STAND_UP_TIME = 1000
    WALKING_TIME = 6000
    TWO_STEP_TIME = len(neurons_coords['FR'])
    ONE_STEP_TIME = TWO_STEP_TIME//2
    INIT_TIME = 10

    is_up = False
    number_of_steps = 0
    Kp = [0, 0, 0]
    Kd = [0, 0, 0]
    rate_count = 0

    while motiontime < 100000:
        # print(motiontime)
        time.sleep(0.002)
        # time.sleep(0.005)
        motiontime += 1
        
        
        udp.Recv()
        udp.GetRecv(state)

        if motiontime >= 0 and motiontime < STAND_UP_TIME + INIT_TIME :
            # print("stand up !!",motiontime)
            motiontime, qInit, state, qDes, d, stand_up_1, rate_count,Kp,Kd = stand_up_procedure(motiontime,qInit,state,qDes,d,stand_up_1,rate_count,Kp,Kd)
        if( motiontime == STAND_UP_TIME + INIT_TIME ): 
           is_up = True
           wake_up_time = motiontime

# # walking phase ---------------------------------------------------------------------
        if is_up and number_of_steps <=15: 
            new_motion_time =  motiontime - wake_up_time
            #retrieve the datas from the foot sensors
            sensor_FL = foot_sensor.get_foot_detected("FL")
            sensor_FR = foot_sensor.get_foot_detected("FR")
            
            if  sensor_FL == "FL foot detected": 
                behavior_walking.push(sensor_FL)
                foot_sensor.reset_detection("FL")

            if sensor_FR == "FR foot detected" : 
                behavior_walking.push(sensor_FR)
                foot_sensor.reset_detection("FR")

            response = behavior_walking.set_new_command()
            if response != []:
                command = response
                i = 0
                behavior_walking.set_ready(False)
                number_of_steps +=1
                print("sending a command ")
            if i < len(command['FR']):


                for part in parts : 
                    qDes[part][0] = command[part][i][0]
                    qDes[part][1] = command[part][i][1]
                    qDes[part][2] = command[part][i][2]
                i += 1

            if i == len(command['FR']) : 
                behavior_walking.set_ready(True)
# 
            # fr_force = state.footForce[0]# real version : uncomment to test in live
            # fl_force = state.footForce[1]# real version : uncomment to test in live
            # rr_force = state.footForce[2]# real version : uncomment to test in live
            # rl_force = state.footForce[3]# real version : uncomment to test in live


            fr_force =  mock_forces['FR'][new_motion_time] # mock version : uncomment to see how behavior walking works !
            fl_force =  mock_forces['FL'][new_motion_time] # mock version : uncomment to see how behavior walking works !
            rr_force =  mock_forces['RR'][new_motion_time] # mock version : uncomment to see how behavior walking works !
            rl_force =  mock_forces['RL'][new_motion_time] # mock version : uncomment to see how behavior walking works !

            forces['FR'].append(fr_force)
            forces['FL'].append(fl_force)
            forces['RR'].append(rr_force)
            forces['RL'].append(rl_force)

            #-----------force treatment and pattern recognition-------------
            # firstly, we just use the sensor of FR limb to make it work
            if new_motion_time%20 == 0: 
                print("new_motion_time :" ,new_motion_time)
            foot_sensor.detect(new_motion_time, fr_force,'FR')
            foot_sensor.detect(new_motion_time, fl_force,'FL')
            # is_step = foot_sensor.retrieve_datas()



            if number_of_steps > 10:  
                if number_of_steps == 11 : 
                    lie_down_time = motiontime
                    rate_count = 0

                    json_path = "data/forces.json"
                    with open(json_path,"w") as json_file: 
                        json.dump(forces,json_file) 

                new_motion_time = motiontime - lie_down_time
                # qDes = lie_down_procedure(new_motion_time,state,qInit,qDes,d,rate_count)
                # design a lie_down_procedure function so that the lie down procedure sends 
                # exactly the same commands to the controllers (you can copy the pattern of
                #  the standu_up_procedure function) 



        for part in parts :  
            cmd.motorCmd[d[ part + '_0' ]].q = qDes[part][0]
            cmd.motorCmd[d[ part + '_0' ]].dq = 0
            cmd.motorCmd[d[ part + '_0' ]].Kp = Kp[0]
            cmd.motorCmd[d[ part + '_0' ]].Kd = Kd[0]
            cmd.motorCmd[d[ part + '_0' ]].tau = -0.65

            cmd.motorCmd[d[ part + '_1' ]].q = qDes[part][1]
            cmd.motorCmd[d[ part + '_1' ]].dq = 0
            cmd.motorCmd[d[ part + '_1' ]].Kp = Kp[1]
            cmd.motorCmd[d[ part + '_1' ]].Kd = Kd[1]
            cmd.motorCmd[d[ part + '_1' ]].tau = 0.0

            cmd.motorCmd[d[ part + '_2' ]].q =  qDes[part][2]
            cmd.motorCmd[d[ part + '_2' ]].dq = 0
            cmd.motorCmd[d[ part + '_2' ]].Kp = Kp[2]
            cmd.motorCmd[d[ part + '_2' ]].Kd = Kd[2]
            cmd.motorCmd[d[ part + '_2' ]].tau = 0.0

        if(motiontime > 10):
            safe.PowerProtect(cmd, state, 1)


        udp.SetSend(cmd)
        udp.Send()