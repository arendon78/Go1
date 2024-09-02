import os 
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt
import json
import time 

from utils import *
from unitree_legged_sdk.example_py.Bezier.foot_trajectory import *
from unitree_legged_sdk.example_py.Bezier.computation_neuron import *
from unitree_legged_sdk.example_py.Bezier.error_calculation import *
from unitree_legged_sdk.example_py.Bezier.plot_neurons import *

from forces.utils_forces import *


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)


from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Frequency_Detector import Frequency_Detector


sys.path.append('../../lib/python/amd64')
import robot_interface as sdk





def main_loop(trajectories,trajectory,TOTAL_OFFSET,neurons_coords,parts,stand_up_1,stand_up_2,stand_up_3):
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
    Kp = [0, 0, 0]
    Kd = [0, 0, 0]

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
    present_frame = []
    p=0


    while motiontime < 20000-1:
        # print(motiontime)
        time.sleep(0.002)
        # time.sleep(0.005)
        motiontime += 1
        
        
        udp.Recv()
        udp.GetRecv(state)

        # coord = trajectory[motiontime%len(trajectory)]

        coords = {'FR': trajectories['FR'][motiontime%len(trajectory)*(TOTAL_OFFSET+1)],
                    'FL': trajectories['FL'][motiontime%len(trajectory)*(TOTAL_OFFSET+1)],
                    'RR': trajectories['RR'][motiontime%len(trajectory)*(TOTAL_OFFSET+1)],
                    'RL': trajectories['RL'][motiontime%len(trajectory)*(TOTAL_OFFSET+1)]
                }
        
        coords2 =  {'FR': neurons_coords['FR'][motiontime%len(trajectory)*(TOTAL_OFFSET+1)],
                    'FL': neurons_coords['FL'][motiontime%len(trajectory)*(TOTAL_OFFSET+1)],
                    'RR': neurons_coords['RR'][motiontime%len(trajectory)*(TOTAL_OFFSET+1)],
                    'RL': neurons_coords['RL'][motiontime%len(trajectory)*(TOTAL_OFFSET+1)]
                }
        
        after_2_step = {   'FR': neurons_coords['FR'][0],
                    'FL': neurons_coords['FL'][0],
                    'RR': neurons_coords['RR'][0],
                    'RL': neurons_coords['RL'][0]
                }
        
        after_1_step = { 'FR': neurons_coords['FR'][len(trajectory)*(0)],
                         'FL': neurons_coords['FL'][len(trajectory)*(1)],
                         'RR': neurons_coords['RR'][len(trajectory)*(1)],
                         'RL': neurons_coords['RL'][len(trajectory)*(0)]
                }
        
        STAND_UP_TIME = 1000
        WALKING_TIME = 6000
        TWO_STEP_TIME = len(neurons_coords['FR'])
        ONE_STEP_TIME = TWO_STEP_TIME//2
        INIT_TIME = 10

        if( motiontime >= 0):
            # print("hey",TWO_STEP_TIME)

            # first, get record initial position------------------)
            if( motiontime >= 0 and motiontime < 10):

                for part in parts : 
                    qInit[part][0] = state.motorState[d[part + '_0']].q
                    qInit[part][1] = state.motorState[d[part + '_1']].q
                    qInit[part][2] = state.motorState[d[part + '_2']].q


#------------------------------------------------------

            if( motiontime >= 10 and motiontime < STAND_UP_TIME +INIT_TIME):
                rate_count += 1
                rate = rate_count/(STAND_UP_TIME//2 - 100)                     # needs count to 500
                Kp = [75, 75, 75]
                Kd = [5, 5, 5]
                
                if (motiontime <=(STAND_UP_TIME+INIT_TIME)//2):
                    for part in parts : 
                        qDes[part][0] = jointLinearInterpolation(qInit[part][0], stand_up_1[part][0], rate)
                        qDes[part][1] = jointLinearInterpolation(qInit[part][1], stand_up_1[part][1], rate)
                        qDes[part][2] = jointLinearInterpolation(qInit[part][2], stand_up_1[part][2], rate)


                if (motiontime == (STAND_UP_TIME+INIT_TIME)//2 ): rate_count = 0

                if (motiontime > (STAND_UP_TIME+INIT_TIME)//2 and motiontime <(STAND_UP_TIME+INIT_TIME)-10):
                    for part in parts : 
                        qDes[part][0] = jointLinearInterpolation(stand_up_1[part][0], stand_up_1[part][0], rate)
                        qDes[part][1] = jointLinearInterpolation(stand_up_1[part][1], stand_up_1[part][1], rate)
                        qDes[part][2] = jointLinearInterpolation(stand_up_1[part][2], stand_up_1[part][2], rate)

                if (motiontime >= (STAND_UP_TIME+INIT_TIME) -10):
                    for part in parts : 
                        qDes[part][0] = jointLinearInterpolation(stand_up_1[part][0], stand_up_1[part][0], rate)
                        qDes[part][1] = jointLinearInterpolation(stand_up_1[part][1], stand_up_1[part][1], rate)
                        qDes[part][2] = jointLinearInterpolation(stand_up_1[part][2], stand_up_1[part][2], rate)


# walking phase ---------------------------------------------------------------------

            if( motiontime >= STAND_UP_TIME + INIT_TIME and motiontime<STAND_UP_TIME + WALKING_TIME + INIT_TIME):
                new_motion_time = motiontime - (STAND_UP_TIME + INIT_TIME)

                
                for number_steps in range(0,WALKING_TIME//(ONE_STEP_TIME),4):
                    if new_motion_time >  number_steps*TWO_STEP_TIME and new_motion_time < (number_steps+1)*TWO_STEP_TIME:
                        # print("1",number_steps,new_motion_time)
                        for part in parts : 
                            qDes[part][0] = jointLinearInterpolation(stand_up_2[part][0], after_2_step[part][0], rate)
                            qDes[part][1] = jointLinearInterpolation(stand_up_2[part][1], after_2_step[part][1], rate)
                            qDes[part][2] = jointLinearInterpolation(stand_up_2[part][2], after_2_step[part][2], rate)

                    elif new_motion_time >  (number_steps+1)*ONE_STEP_TIME and new_motion_time < (number_steps+2)*ONE_STEP_TIME:
                        # print("2",number_steps+1,new_motion_time)
                        for part in parts :
                            if (new_motion_time == (number_steps+1)*ONE_STEP_TIME +1) : 
                                start = time.time()
                                print("this is the time when the first command of a foot trajectory was sent : ", new_motion_time)
                            qDes[part][0] = coords2[part][0]
                            qDes[part][1] = coords2[part][1]
                            qDes[part][2] = coords2[part][2]
                            # print("command sent to robot : ",qDes[part][0], qDes[part][1],qDes[part][2])

                    elif new_motion_time >  (number_steps+2)*ONE_STEP_TIME and new_motion_time < (number_steps+3)*ONE_STEP_TIME:
                        # print("1",number_steps,new_motion_time)
                        for part in parts : 
                            qDes[part][0] = jointLinearInterpolation(stand_up_2[part][0], after_2_step[part][0], rate)
                            qDes[part][1] = jointLinearInterpolation(stand_up_2[part][1], after_2_step[part][1], rate)
                            qDes[part][2] = jointLinearInterpolation(stand_up_2[part][2], after_2_step[part][2], rate)

                fr_force = state.footForce[0]
                fl_force = state.footForce[1]
                rr_force = state.footForce[2]
                rl_force = state.footForce[3]

                forces['FR'].append(fr_force)
                forces['FL'].append(fl_force)
                forces['RR'].append(rr_force)
                forces['RL'].append(rl_force)

                #-----------force treatment and pattern recognition-------------
                # firstly, we just use the sensor of FR limb to make it work

                if new_motion_time == 0 : 
                    new_point = [new_motion_time,fr_force]
                else : 
                    old_point = new_point

                    new_point = [new_motion_time, fr_force]

                    old_point =  old_point + [calculate_derivative(new_point,old_point)]

                    #---you have a delay of 1 point...
                    
                    present_frame.append(old_point)

                    if len(present_frame)%40 == 0 : 
                        local_maxes = monte_carlo_gradient(1,present_frame)
                        local_mins = monte_carlo_gradient(-1,present_frame)

                        new_merged_mins_maxes_coordinates = build_merge(local_maxes, local_mins)
                        bool, p0,p1,p2 = find_a_pattern(new_merged_mins_maxes_coordinates, present_frame,500,500,4)

                        if bool : 
                            # print("pattern found !\n\n",p0,p1,p2)#-----------this is typically where we would take action after the recognition of a step.
                            end = time.time()
                            print("time delay : ",end-start)
                            print("pattern found ! at : ", new_motion_time)
                            p+=1
                            old_frame += present_frame
                            present_frame = []
                        
# 
# 
                # for part in parts :
                #     qDes[part][0] = coords2[part][0]
                #     qDes[part][1] = coords2[part][1]
                #     qDes[part][2] = coords2[part][2]
                #     print("command sent to robot : ",qDes[part][0], qDes[part][1],qDes[part][2])

#------------------------------------------------------------------------------------------------------
            if (motiontime == STAND_UP_TIME + WALKING_TIME +INIT_TIME -1 ) : 
                rate_count=0
                #saving forces datas
                json_path = "data/forces.json"
                with open(json_path,"w") as json_file: 
                    json.dump(forces,json_file) 
                #--------               
#---------------------------------------------------------------------------

            if (motiontime >= STAND_UP_TIME + WALKING_TIME +INIT_TIME and motiontime < STAND_UP_TIME + WALKING_TIME + 2 * INIT_TIME):
                for part in parts : 
                    qInit[part][0] = state.motorState[d[part + '_0']].q
                    qInit[part][1] = state.motorState[d[part + '_1']].q
                    qInit[part][2] = state.motorState[d[part + '_2']].q

            if (motiontime >=STAND_UP_TIME + WALKING_TIME + 2*INIT_TIME):
                rate_count += 1
                rate = rate_count/STAND_UP_TIME            # needs count to 200



                sign = 1
                for part in parts : 
                    qDes[part][0] = jointLinearInterpolation(qInit[part][0], sign* -0.3161579668521881, rate)
                    qDes[part][1] = jointLinearInterpolation(qInit[part][1], 1.208921194076538, rate)
                    qDes[part][2] = jointLinearInterpolation(qInit[part][2], -2.7958271503448486, rate)
                    sign = sign * -1


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
            print(qDes['FR'])
            fr_force = state.footForce[0]

            print(fr_force)
            assert qDes['FR'] == qDes['FL']
            assert qDes['FL'] == qDes['RR']
            assert qDes['RR'] == qDes['RL']

        if(motiontime > 10):
            safe.PowerProtect(cmd, state, 1)


        udp.SetSend(cmd)
        udp.Send()
        if (motiontime >20000): 
            break