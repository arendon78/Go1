#!/usr/bin/python
import os 
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)


from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator

from Neuroscience.structures.Frequency_Detector import Frequency_Detector
from Neuroscience.structures.Controller import Controller


sys.path.append('../lib/python/amd64')
import robot_interface as sdk

def jointLinearInterpolation(initPos, targetPos, rate):

    rate = np.fmin(np.fmax(rate, 0.0), 1.0)
    p = initPos*(1-rate) + targetPos*rate
    return p

import math

def theta_hip(z, y):
    """
    Calculate the hip angle θ_hip.
    
    Parameters:
    z (float): The z-coordinate.
    y (float): The y-coordinate.
    
    Returns:
    float: The hip angle θ_hip in radians.
    """
    return math.atan2(z, y)

def theta_thigh(x, y, z, L=0.213):
    """
    Calculate the thigh angle θ_thigh.
    
    Parameters:
    x (float): The x-coordinate.
    y (float): The y-coordinate.
    z (float): The z-coordinate.
    L (float): The length parameter, default is 0.213.
    
    Returns:
    float: The thigh angle θ_thigh in radians.
    """
    distance = math.sqrt(x**2 + y**2 + z**2)
    cos_term = distance / (2 * L)
    # Ensure cos_term is within the valid range for acos
    cos_term = min(1.0, max(-1.0, cos_term))
    term1 = math.acos(cos_term)
    term2 = math.atan2(-x, math.sqrt(y**2 + z**2))
    return term1 + term2

def theta_calf(x, y, z, L=0.213):
    """
    Calculate the calf angle θ_calf.
    
    Parameters:
    x (float): The x-coordinate.
    y (float): The y-coordinate.
    z (float): The z-coordinate.
    L (float): The length parameter, default is 0.213.
    
    Returns:
    float: The calf angle θ_calf in radians.
    """
    thigh_angle = theta_thigh(x, y, z, L)
    sin_term = (-x / L) - math.sin(thigh_angle)
    # Ensure sin_term is within the valid range for asin
    sin_term = min(1.0, max(-1.0, sin_term))
    term1 = math.asin(sin_term)
    return term1 - thigh_angle




if __name__ == '__main__':
    sim_time = 2500
    N_REPEAT = 4

    N_SIM = 90


    ## enculé
    V = [[np.zeros([N_SIM*(sim_time-400), 1]) for _ in range(3)] for _ in range(4)]

    ## enculé

    # Neurons intialisation
    #--------------------------------
    res = 0.1

    inputs = np.zeros([sim_time,1])
    inputs[1]=1

    ctrl = Controller(res)
    ctrl.create_oscillators(0.25)

    watch = Frequency_Detector(res ,controller = ctrl)

    #---------------------------------

    d = {'FR_0':0, 'FR_1':1, 'FR_2':2,
         'FL_0':3, 'FL_1':4, 'FL_2':5, 
         'RR_0':6, 'RR_1':7, 'RR_2':8, 
         'RL_0':9, 'RL_1':10, 'RL_2':11 }
    PosStopF  = math.pow(10,9)
    VelStopF  = 16000.0
    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff
    sin_mid_q = [0, 0.7,-1.7]
    dt = 0.002
    qInit = [0, 0, 0]
    qDes = [0, 0, 0]
    sin_count = 0
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
    inputs = np.zeros([sim_time,1])            #Initialize V.

    a = [0]
    b=[0]
    ## main loop


    internal_time = 0
    while motiontime < sim_time-1:
        # print(motiontime)
        # print((motiontime//1000)/10 )
        time.sleep(0.002)

        # print(motiontime)
        # print(state.imu.rpy[0])
        
        
        udp.Recv()
        udp.GetRecv(state)

        #Neurons
        # ctrl.pass_inputs(inputs[motiontime])



        if( motiontime >= 0):
            # print(len(V)) 
            print(motiontime)
            if (motiontime < 400):
                a.append(0)
                b.append(0)

            # first, get record initial position
            if( motiontime >= 0 and motiontime < 10):
                qInit[0] = state.motorState[d['RR_0']].q
                qInit[1] = state.motorState[d['RR_1']].q
                qInit[2] = state.motorState[d['RR_2']].q
            
            # second, move to the origin point of a sine movement with Kp Kd
            if( motiontime >= 10 and motiontime < 400):
                rate_count += 1
                rate = rate_count/200.0                       # needs count to 200
                Kp = [5, 5, 5]
                Kd = [1, 1, 1]
                # Kp = [20, 20, 20]
                # Kd = [2, 2, 2]
                
                
                qDes[0] = jointLinearInterpolation(qInit[0], sin_mid_q[0], rate)
                qDes[1] = jointLinearInterpolation(qInit[1], sin_mid_q[1], rate)
                qDes[2] = jointLinearInterpolation(qInit[2], sin_mid_q[2], rate)
            

            if( motiontime >= 400):
                A_N1 = 1.4
                A_N2 = 0.5
                new_motion_time = motiontime - 400

                # print(new_motion_time)
                w = 2*math.pi/100
                n1  = A_N1*math.sin(new_motion_time*w)
                n2 = n1/A_N1
                print("sin : ",math.sin(new_motion_time/500))

                if new_motion_time % (15) ==0:
                    # print("zero here\n\n\n")
                    ctrl.create_oscillators(n2)
                    ctrl.pass_inputs(1)
                else : 
                    # print("not zeero")
                    ctrl.pass_inputs(0)

                # print(new_motion_time)

                
                ctrl.simulate(internal_time,V)
                watch.update_firing_rate()
                contraction_ratio = watch.frequency_ratio()
                internal_time +=1
                
                for i in range(0,N_SIM-1):
                    ctrl.pass_inputs(0)
                    ctrl.simulate(internal_time,V)
                    watch.update_firing_rate()
                    contraction_ratio = watch.frequency_ratio()
                    internal_time+=1

                # ctrl.pass_inputs(0)
                # ctrl.simulate(internal_time,V)
                # watch.update_firing_rate()
                # contraction_ratio = watch.frequency_ratio()
                # internal_time+=1

                # ctrl.pass_inputs(0)
                # ctrl.simulate(internal_time,V)
                # watch.update_firing_rate()
                # contraction_ratio = watch.frequency_ratio()
                # internal_time+=1

                a.append(contraction_ratio)
                b.append(n2)
                print(contraction_ratio)

                z = 0
                y = 27.4
                x = 20
                
                # remplacer ça par un truc qui va générer le bon mouvement et un qui va regarder et générer le bon output.
            
                qDes[0] = theta_hip(z,y)
                # qDes[1] = theta_thigh(x,y,z)
                qDes[1] = sin_mid_q[1] + A_N1*contraction_ratio
                # qDes[1] = sin_mid_q[1] + n1
                # qDes[2]  = theta_calf(x,y,z)
                qDes[2] = sin_mid_q[2] #+ 0.5*math.sin(new_motion_time/200 + math.pi/2)


                # print(f"θ_hip: {qDes[0]} radians")
                # print(f"θ_thigh: {qDes[1]} radians")
                # print(f"θ_calf: {qDes[2]} radians")

            

            cmd.motorCmd[d['FL_0']].q = qDes[0]
            cmd.motorCmd[d['FL_0']].dq = 0
            cmd.motorCmd[d['FL_0']].Kp = Kp[0]
            cmd.motorCmd[d['FL_0']].Kd = Kd[0]
            cmd.motorCmd[d['FL_0']].tau = -0.65

            cmd.motorCmd[d['FL_1']].q = qDes[1]
            cmd.motorCmd[d['FL_1']].dq = 0
            cmd.motorCmd[d['FL_1']].Kp = Kp[1]
            cmd.motorCmd[d['FL_1']].Kd = Kd[1]
            cmd.motorCmd[d['FL_1']].tau = 0.0

            cmd.motorCmd[d['FL_2']].q =  qDes[2]
            cmd.motorCmd[d['FL_2']].dq = 0
            cmd.motorCmd[d['FL_2']].Kp = Kp[2]
            cmd.motorCmd[d['FL_2']].Kd = Kd[2]
            cmd.motorCmd[d['FL_2']].tau = 0.0
            # cmd.motorCmd[d['FR_2']].tau = 2 * sin(t*freq_rad)


        if(motiontime > 10):
            safe.PowerProtect(cmd, state, 1)

        udp.SetSend(cmd)
        udp.Send()
        motiontime += 1

    t = np.arange(0,sim_time)*1         #Define the time axis.
    # b = np.arange(0,sim_time)*
    plt.figure()                         #Plot the results.
    plt.plot(t,a,b)
    plt.xlabel('Time [ms]')
    plt.ylabel('Voltage [mV]');
    plt.show()
