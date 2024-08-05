import os 
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt

from utils import *
from foot_trajectory import *
from computation_neuron import *
from error_calculation import *
from plot_neurons import *
from main_loop import *


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)


from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Frequency_Detector import Frequency_Detector


sys.path.append('../../lib/python/amd64')
import robot_interface as sdk



def main_loop(trajectories,trajectory,TOTAL_OFFSET,neurons_coords,parts,stand_up_1,stand_up_2,stand_up_3):
    
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



    while motiontime < 20000-1:
        print(motiontime)
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
        
        STAND_UP_TIME = 1000
        WALKING_TIME = 1000
        INIT_TIME = 10

        if( motiontime >= 0):

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
                        qDes[part][0] = jointLinearInterpolation(stand_up_1[part][0], stand_up_2[part][0], rate)
                        qDes[part][1] = jointLinearInterpolation(stand_up_1[part][1], stand_up_2[part][1], rate)
                        qDes[part][2] = jointLinearInterpolation(stand_up_1[part][2], stand_up_2[part][2], rate)

                if (motiontime >= (STAND_UP_TIME+INIT_TIME) -10):
                    for part in parts : 
                        qDes[part][0] = jointLinearInterpolation(stand_up_2[part][0], stand_up_3[part][0], rate)
                        qDes[part][1] = jointLinearInterpolation(stand_up_2[part][1], stand_up_3[part][1], rate)
                        qDes[part][2] = jointLinearInterpolation(stand_up_2[part][2], stand_up_3[part][2], rate)


# walking phase ---------------------------------------------------------------------

            if( motiontime >= STAND_UP_TIME + INIT_TIME and motiontime<STAND_UP_TIME + WALKING_TIME + INIT_TIME):
                new_motion_time = motiontime - (STAND_UP_TIME + INIT_TIME)
                # print(new_motion_time)
                # 
# 
                for part in parts :
                    # x = coords[part][0]
                    # y = coords[part][1]
                    # z = 0
                    # # for number in ['_0','_1','_2']: 
                    # qDes[part][0] = z
                    # qDes[part][1] = theta_thigh(x,y,z)
                    # qDes[part][2] = theta_calf(x,y,z)

                    qDes[part][0] = 0
                    qDes[part][1] = coords2[part][0]
                    qDes[part][2] = coords2[part][1]
                    # distance += math.sqrt((qDes[part][1]-coords2[part][0])**2 + (qDes[part][2]-coords2[part][1])**2)
                    # print(stand_up_2[part][2])
#------------------------------------------------------------------------------------------------------
            if (motiontime == STAND_UP_TIME + WALKING_TIME +INIT_TIME -1 ) : rate_count=0
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

        if(motiontime > 10):
            safe.PowerProtect(cmd, state, 1)


        udp.SetSend(cmd)
        udp.Send()
        if (motiontime >20000): 
            break