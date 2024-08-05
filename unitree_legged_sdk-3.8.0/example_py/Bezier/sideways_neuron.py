#!/usr/bin/python
import os 
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt

from utils import *
from foot_trajectory import *


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)


from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator
from Neuroscience.structures.Controller_old import Controller
from Neuroscience.structures.Frequency_Detector_old import Frequency_Detector


sys.path.append('../../lib/python/amd64')
import robot_interface as sdk




if __name__ == '__main__':
    # standx = -0.045
    standx = -0.048
    Lspan= 0.025
    deltaL = 0.02
    delta= 0.02
    standy= -0.35
    Yspan= 0.04
    deltaY= 0.01

    # NUM_POINST_BEZIER = 50
    # NUM_POINTS_STANCE = 50

    NUM_POINST_BEZIER = 5
    NUM_POINTS_STANCE = 5

    trajectory = generate_trajectory(standx, Lspan, deltaL, delta, standy, Yspan, deltaY,num_points_bezier=NUM_POINST_BEZIER, num_points_stance= NUM_POINTS_STANCE)
    
    #the generate_function trajctory is made for a forward gait. To generate a sideways gate, we just change one coordinate.



    # control_points = [(-0.07, -0.34), 
    #                   (-0.09, -0.34), 
    #                   (-0.1, -0.3), (-0.1, -0.3),(-0.1, -0.3),
    #                   (-0.045, -0.3),(-0.045, -0.3),
    #                   (-0.045,-0.29),
    #                   (0,-0.29),(0,-0.29),
    #                   (-0.01,-0.34),
    #                   (-0.03,-0.34)]

    control_points = generate_control_points(standx, Lspan, deltaL, delta, standy, Yspan, deltaY)

    bezier_curve_points = bezier(control_points)
    stance_curve_points = stance_phase(bezier_curve_points[-1], bezier_curve_points[0])

    plot_trajectory(control_points, bezier_curve_points, stance_curve_points)     
    plot_trajectory_2(trajectory)   
    plot_trajectory_3(bezier_curve_points,stance_curve_points)
    plot_trajectory_single(trajectory,(0,1),"zde","fez")

    d = {'FR_0':0, 'FR_1':1, 'FR_2':2,
         'FL_0':3, 'FL_1':4, 'FL_2':5, 
         'RR_0':6, 'RR_1':7, 'RR_2':8, 
         'RL_0':9, 'RL_1':10, 'RL_2':11 }
    

    PosStopF  = math.pow(10,9)
    VelStopF  = 16000.0
    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff

    bias_default = 0

    stand_up_2 = {'FR' : [0, theta_thigh(0,trajectory[0][0],trajectory[0][1]), theta_calf(0,trajectory[0][0],trajectory[0][1])] , 
                  'FL' : [0, theta_thigh(0,trajectory[0][0],trajectory[0][1]), theta_calf(0,trajectory[0][0],trajectory[0][1])] ,
                  'RR' : [0, theta_thigh(0,trajectory[0][0],trajectory[0][1]), theta_calf(0,trajectory[0][0],trajectory[0][1])] , 
                  'RL' : [0, theta_thigh(0,trajectory[0][0],trajectory[0][1]), theta_calf(0,trajectory[0][0],trajectory[0][1])] 
                  }
    stand_up_1 = stand_up_2
    stand_up_3 = stand_up_2
    dt = 0.002


    qInit = [0, 0, 0]
    qDes = [0, 0, 0]
    limbs = ['FR_0', 'FR_1', 'FR_2', 
         'FL_0', 'FL_1', 'FL_2', 
         'RR_0', 'RR_1', 'RR_2', 
         'RL_0', 'RL_1', 'RL_2']
    
    parts = ['FR','FL','RR','RL']   

    qInit = {parts[i] : [0,0,0] for i in range(len(parts))}
    
    qDes = {parts[i] : [0,0,0] for i in range(len(parts))}
    # print(qInit)
    # print(qDes)

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

    offset_cycle_FR = 0
    offset_cycle_FL = 1
    offset_cycle_RR = 1
    offset_cycle_RL = 0

    TOTAL_OFFSET = 1

    FR_trajectory = unphase(0,trajectory)
    FL_trajectory = unphase(0,trajectory)
    RR_trajectory = unphase(0,trajectory)
    RL_trajectory = unphase(0,trajectory)

    trajectories = {
                    'FR': [trajectory[0]]* len(trajectory) * offset_cycle_FR +  FR_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_FR ) ,
                    'FL': [trajectory[0]]* len(trajectory) * offset_cycle_FL +  FL_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_FL ),
                    'RR': [trajectory[0]]* len(trajectory) * offset_cycle_RR +  RR_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_RR ),
                    'RL': [trajectory[0]]* len(trajectory) * offset_cycle_RL +  RL_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_RL )
                    }
    

        # FR hip :  -0.3161579668521881
        # FR tihgh :  1.208921194076538
        # FR calf :  -2.7958271503448486
        # FL hip :  0.30471307039260864
        # FL tihgh :  1.2391986846923828
        # FL calf :  -2.8132669925689697
        # RR hip :  -0.3770763576030731
        # RR tihgh :  1.22036612033844
        # RR calf :  -2.797118902206421
        # RL hip :  0.35830429196357727
        # RL tihgh :  1.224181056022644
        # RL calf :  -2.787914514541626

    #neurons ------------------------

    #instanciation
    res = 0.1

    controllers = { part : [Controller(res),
                            Controller(res),
                            Controller(res)]
                    for part in parts }
    
    [[controllers[part][i].create_oscillators(0.25) for part in parts ] for i in range(3) ]
    # to each articulation : associates a controller

    V = [[np.zeros([(20000), 1]) for _ in range(3)] for _ in range(5)]
    #mock V : do not plot it it won't work.

    # voltages = {part : [V,V,V] for part in parts }

    watchers = { part : [Frequency_Detector(res ,controller = controllers[part][0]),
                         Frequency_Detector(res ,controller = controllers[part][1]),
                         Frequency_Detector(res ,controller = controllers[part][2])] 
                for part in parts }
    # to each articulation : associates a frequency detector


    # computing the path to follow based on the previously generated trajectory.

    neurons_coords = {  'FR' : [],
                        'FL' : [],
                        'RR' : [],
                        'RL' : []
    }

    command_coords = {  'FR' : [],
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

    print("\n\n -------- computation loop ---------- \n\n")


    #computation loop

    print(len(trajectory)*(TOTAL_OFFSET+1),"steps to simulate")

    for i in range(len(trajectory)*(TOTAL_OFFSET+1)): 

        coords = {'FR': trajectories['FR'][i],
            'FL': trajectories['FL'][i],
            'RR': trajectories['RR'][i],
            'RL': trajectories['RL'][i]
        }


        print(i)
        # for part in parts : 
        for part in ['FR','FL','RR','RL']:

            
            internal_time = 0

            # print(internal_time)
            # x = coords[part][0]
            # y = coords[part][1]
            # z = 0

            x = 0 
            y = coords[part][1] # the part that make you go up and down
            z = coords[part][0] #the part of the movement that makes you move


            hip = theta_hip(x,y,z)
            thigh = x
            calf = theta_calf(x,y,z)


            inside_oscillator_hip = controllers[part][0].create_oscillators(hip)
            controllers[part][0].pass_inputs(1)
            controllers[part][0].simulate(internal_time,V)
            frequency_parts[part][0].append(watchers[part][0].frequency_ratio())

            inside_oscillator_thigh = controllers[part][1].create_oscillators(thigh)
            controllers[part][1].pass_inputs(1)
            controllers[part][1].simulate(internal_time,V)
            frequency_parts[part][1].append(watchers[part][1].frequency_ratio())

            inside_oscillator_calf = controllers[part][2].create_oscillators(calf)
            controllers[part][2].pass_inputs(1)
            controllers[part][2].simulate(internal_time,V)
            frequency_parts[part][2].append(watchers[part][2].frequency_ratio())
            
            internal_time+=1
            #simulate them for a reasonable time
            # problem : simulates all the neurons. should only simulate one neuron at a time (the one that is active)
            for j in range( 1000 ) : 

                inside_oscillator[part][0].append(inside_oscillator_hip)
                inside_oscillator[part][1].append(inside_oscillator_thigh)
                inside_oscillator[part][2].append(inside_oscillator_calf)

                watchers[part][0].update_firing_rate(j)
                controllers[part][0].pass_inputs(0)
                controllers[part][0].simulate(internal_time,V)
                frequency_parts[part][0].append(watchers[part][0].frequency_ratio())
                command[part][0].append(hip)


                watchers[part][1].update_firing_rate(j)
                controllers[part][1].pass_inputs(0)
                controllers[part][1].simulate(internal_time,V)
                frequency_parts[part][1].append(watchers[part][1].frequency_ratio())
                command[part][1].append(thigh)


                watchers[part][2].update_firing_rate(j)
                controllers[part][2].pass_inputs(0)
                controllers[part][2].simulate(internal_time,V)
                frequency_parts[part][2].append(watchers[part][2].frequency_ratio())
                command[part][2].append(calf)

                internal_time+=1


            neuron_hip = watchers[part][0].frequency_ratio   ()
            neuron_thigh = watchers[part][1].frequency_ratio ()
            neuron_calf  = watchers[part][2].frequency_ratio ()
            
            #I don't care about neuron_hip in the first place
            
            neurons_coords[part].append((neuron_hip,neuron_calf))
            command_coords[part].append((hip,calf))

    #plot the coords from neurons : 
    

    plot_trajectory_single(neurons_coords['FR'],(0,1),"dzde","fezdz")
    plot_trajectory_single(command_coords['FR'],(0,1),"dzde","fezdz")

    freq0 = np.array(frequency_parts['FR'][0])
    freq1 = np.array(frequency_parts['FR'][1])
    freq2 = np.array(frequency_parts['FR'][2])

    oscillator0_data = np.array(inside_oscillator['FR'][0])
    oscillator1_data = np.array(inside_oscillator['FR'][1])
    oscillator2_data = np.array(inside_oscillator['FR'][2])

    freq_command0 = np.array(command['FR'][0])
    freq_command1 = np.array(command['FR'][1])
    freq_command2 = np.array(command['FR'][2])


    xfreq0 =np.arange(len(freq0))
    xfreq1 = np.arange(len(freq1)) # x1
    xfreq2 = np.arange(len(freq2)) # x2
    xfreq_command0 = np.arange(len(freq_command0))
    xfreq_command1 = np.arange(len(freq_command1)) # x3
    xfreq_command2 = np.arange(len(freq_command2)) # x4
    xoscillator0_data = np.arange(len(oscillator0_data))
    xoscillator1_data = np.arange(len(oscillator1_data)) # x5
    xoscillator2_data = np.arange(len(oscillator2_data)) # x6


    # Créer une figure avec 2 sous-graphiques (2 lignes, 1 colonne)
    fig1, (ax0,ax1, ax2) = plt.subplots(3, 1, figsize=(12, 6))

    ax0.plot(xfreq0, freq0, color="blue", label="Freq 0")
    ax0.plot(xfreq_command0, freq_command0, color="green", label="Command 0")
    ax0.plot(xoscillator0_data, oscillator0_data, color="red", label="Oscillator 0")
    ax0.set_ylabel("Position and Frequency on hip")
    ax0.legend()

    # Tracer les données dans le premier sous-graphe (ax1)
    ax1.plot(xfreq1, freq1, color="blue", label="Freq 1")
    ax1.plot(xfreq_command1, freq_command1, color="green", label="Command 1")
    ax1.plot(xoscillator1_data, oscillator1_data, color="red", label="Oscillator 1")
    ax1.set_ylabel("Position and Frequency on tigh")
    ax1.legend()

    # Tracer les données dans le deuxième sous-graphe (ax2)
    ax2.plot(xfreq2, freq2, color="blue", label="Freq 2")
    ax2.plot(xfreq_command2, freq_command2, color="green", label="Command 2")
    ax2.plot(xoscillator2_data, oscillator2_data, color="red", label="Oscillator 2")
    ax2.set_ylabel("Position and Frequency on calf")
    ax2.legend()

    plt.tight_layout()
    plt.show()


    #------------------------

    #computing MAE and MSE

    n= len(oscillator1_data)
    print(len(oscillator1_data))
    print(len(freq_command1))
    assert (len(oscillator1_data) == len(freq_command1))
    sum_absolute_error = 0
    squarred_error = 0
    maximum_error = -1
    for i in range(n): 
        absolute_error = abs(oscillator1_data[i] - freq_command1[i] )
        sum_absolute_error += absolute_error
        if absolute_error> maximum_error : 
            maximum_error = absolute_error
        
        squarred_error+= (oscillator1_data[i] - freq_command1[i]) * (oscillator1_data[i] - freq_command1[i])

    result_MAE = sum_absolute_error / n
    result_MSE = squarred_error / n

    print("MAE : ", result_MAE)
    print("MSE : ", result_MSE)
    print("maximum error : ",maximum_error)

    amplitude = max(freq_command1) - min(freq_command1)

    print("relative MAE (percentage) : ", str((result_MAE / amplitude)*100)[:5], "%")
    input("To begin the walking gait, press enter")




    print("\n\n -------- main loop ---------- \n\n")

    ## main loop
    distance = 0
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


# #walking phase  : neuronless ---------------------------------------------------------------------

#             if( motiontime >= STAND_UP_TIME + INIT_TIME and motiontime<STAND_UP_TIME + WALKING_TIME + INIT_TIME):
#                 new_motion_time = motiontime - (STAND_UP_TIME + INIT_TIME)
#                 print(new_motion_time)
#                 # 
# # 
#                 for part in parts :
# # 
#                     x = coords[part][0]
#                     y = coords[part][1]
#                     z = 0
# # 
#                     # for number in ['_0','_1','_2']: 
#                     qDes[part][0] = z
#                     qDes[part][1] = theta_thigh(x,y,z)
#                     qDes[part][2] = theta_calf(x,y,z)
#                     print(stand_up_2[part][2])
# #------------------------------------------------------------------------------------------------------

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

                    qDes[part][0] = coords2[part][0]
                    qDes[part][1] = 0
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
    print("mean distance : ",distance/20000)
