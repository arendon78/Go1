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


sys.path.append('../lib/python/amd64')
import robot_interface as sdk

def jointLinearInterpolation(initPos, targetPos, rate):

    rate = np.fmin(np.fmax(rate, 0.0), 1.0)
    p = initPos*(1-rate) + targetPos*rate
    return p


if __name__ == '__main__':


    # Neurons intialisation
    #--------------------------------
    res = 0.1

    oscillator = Tunable_Oscillator(res = res)
    oscillator.tune(2,[10,10])
    oscillator.brain[0].taken_inputs[1] = 1
    freq = Frequency_Detector(res,[oscillator.brain[2]])

    #---------------------------------

    d = {'FR_0':3, 'FR_1':4, 'FR_2':5,
         'FL_0':3, 'FL_1':4, 'FL_2':5, 
         'RR_0':6, 'RR_1':7, 'RR_2':8, 
         'RL_0':9, 'RL_1':10, 'RL_2':11 }
    PosStopF  = math.pow(10,9)
    VelStopF  = 16000.0
    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff
    sin_mid_q = [0.8, 3.5, -1]
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
    sim_time = 10000
    V = [np.zeros([sim_time,1]), np.zeros([sim_time,1]), np.zeros([sim_time,1])]
    inputs = np.zeros([sim_time,1])            #Initialize V.
    inputs[1] = [1]


    ## main loop
    while motiontime < sim_time-1:
        print(motiontime)
        # print((motiontime//1000)/10 )
        time.sleep(0.002)
        motiontime += 1

        # print(motiontime)
        # print(state.imu.rpy[0])
        
        
        udp.Recv()
        udp.GetRecv(state)

        #Neurons

        freq.update_firing_rate()
        oscillator.brain[0].inputs[1] = inputs[motiontime]

        oscillator.simulate(motiontime,V)

        contraction_ratio = freq.frequency_ratio()



        if( motiontime >= 0):

            # first, get record initial position
            if( motiontime >= 0 and motiontime < 10):
                qInit[0] = state.motorState[d['FR_0']].q
                qInit[1] = state.motorState[d['FR_1']].q
                qInit[2] = state.motorState[d['FR_2']].q
            
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
                

                qDes[0] = sin_mid_q[0] 
                qDes[1] = sin_mid_q[1]  
                qDes[2] = sin_mid_q[2] + (motiontime//1000)/10

            

            cmd.motorCmd[d['FR_0']].q = qDes[0]
            cmd.motorCmd[d['FR_0']].dq = 0
            cmd.motorCmd[d['FR_0']].Kp = Kp[0]
            cmd.motorCmd[d['FR_0']].Kd = Kd[0]
            cmd.motorCmd[d['FR_0']].tau = -0.65

            cmd.motorCmd[d['FR_1']].q = qDes[1]
            cmd.motorCmd[d['FR_1']].dq = 0
            cmd.motorCmd[d['FR_1']].Kp = Kp[1]
            cmd.motorCmd[d['FR_1']].Kd = Kd[1]
            cmd.motorCmd[d['FR_1']].tau = 0.0

            cmd.motorCmd[d['FR_2']].q =  qDes[2]
            cmd.motorCmd[d['FR_2']].dq = 0
            cmd.motorCmd[d['FR_2']].Kp = Kp[2]
            cmd.motorCmd[d['FR_2']].Kd = Kd[2]
            cmd.motorCmd[d['FR_2']].tau = 0.0
            # cmd.motorCmd[d['FR_2']].tau = 2 * sin(t*freq_rad)


        if(motiontime > 10):
            safe.PowerProtect(cmd, state, 1)

        udp.SetSend(cmd)
        udp.Send()

for i in range(len(oscillator.brain)):
    t = np.arange(0,len(V[i]))*res          #Define the time axis.

    plt.figure()                         #Plot the results.
    plt.plot(t,V[i])
    plt.xlabel('Time [ms]')
    plt.ylabel('Voltage [mV]');
    plt.show()
