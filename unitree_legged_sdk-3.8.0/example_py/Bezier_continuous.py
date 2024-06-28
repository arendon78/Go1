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


import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def bezier(points, num_points=100):
    """
    Generates a Bézier curve from a list of control points.

    Parameters:
    points (list of tuples): List of control points (x, y).
    num_points (int): Number of points to generate along the curve.

    Returns:
    list of tuples: Points on the Bézier curve.
    """

    n = len(points) - 1
    t_values = np.linspace(0, 1, num_points)
    curve_points = []

    for t in t_values:
        x = sum(comb(n, i) * (1 - t)**(n - i) * t**i * points[i][0] for i in range(n + 1))
        y = sum(comb(n, i) * (1 - t)**(n - i) * t**i * points[i][1] for i in range(n + 1))
        curve_points.append((x, y))

    return curve_points



def stance_phase(start_point, end_point, num_points=100, delta = 0.007):
    """
    Generates a stance-phase trajectory using a sinusoidal function.

    Parameters:
    start_point (tuple): The starting point of the stance phase.
    end_point (tuple): The ending point of the stance phase.
    num_points (int): Number of points to generate along the stance trajectory.
    amplitude (float): Amplitude of the sinusoidal function.

    Returns:
    list of tuples: Points on the stance-phase trajectory.
    """

    x_start, y_start = start_point
    x_end, y_end = end_point
    x_values = np.linspace(x_start, x_end, num_points)
    y_values = y_start - delta * np.sin(np.pi * np.linspace(0, 1, num_points))

    return list(zip(x_values, y_values))



def plot_trajectory(control_points, bezier_points, stance_points):
    """
    Plots the swing and stance phases of the foot trajectory.

    Parameters:
    control_points (list of tuples): Control points for the Bézier curve.
    bezier_points (list of tuples): Points on the Bézier curve (swing phase).
    stance_points (list of tuples): Points on the stance phase trajectory.
    """
    control_points = np.array(control_points)
    bezier_curve = np.array(bezier_points)
    stance_curve = np.array(stance_points)

    plt.plot(control_points[:, 0], control_points[:, 1], 'ro--', label='Control Points')
    plt.plot(bezier_curve[:, 0], bezier_curve[:, 1], 'b-', label='Swing Phase')
    plt.plot(stance_curve[:, 0], stance_curve[:, 1], 'r-', label='Stance Phase')
    plt.legend()
    plt.xlabel('X coordinate WRT hip (m)')
    plt.ylabel('Y coordinate WRT hip (m)')
    plt.title('Sample Foot Trajectory Generation')
    plt.show()



def generate_control_points(standx, Lspan, deltaL, delta, standy, Yspan, deltaY):
    """
    Generates control points for the Bézier curve based on given parameters.

    Parameters:
    standx (float): Stand x-coordinate.
    Lspan (float): Span in the x-direction.
    deltaL (float): Change in the x-direction for some points.
    delta (float): Small delta for some y-coordinates.
    standy (float): Stand y-coordinate.
    Yspan (float): Span in the y-direction.
    deltaY (float): Change in the y-direction for some points.

    Returns:
    list of tuples: Control points.
    """
    points = [
        (standx - Lspan, standy),  # 0
        (standx - Lspan - deltaL, standy),  # 1
        (standx - Lspan - deltaL - delta, standy + Yspan),  # 2
        (standx - Lspan - deltaL - delta, standy + Yspan),  # 3
        (standx - Lspan - deltaL - delta, standy + Yspan),  # 4
        (standx, standy + Yspan),  # 5
        (standx, standy + Yspan),  # 6
        (standx, standy + Yspan + deltaY),  # 7
        (standx + Lspan + deltaL + delta, standy + Yspan + deltaY),  # 8
        (standx + Lspan + deltaL + delta, standy + Yspan + deltaY),  # 9
        (standx + Lspan + deltaL, standy),  # 10
        (standx + Lspan, standy)  # 11
    ]
    return points

def generate_trajectory(standx, Lspan, deltaL, delta, standy, Yspan, deltaY):
    points = generate_control_points(standx, Lspan, deltaL, delta, standy, Yspan, deltaY)
    bezier_curve_points = bezier(points)
    stance_curve_points = stance_phase(bezier_curve_points[-1], bezier_curve_points[0],delta=delta)

    return bezier_curve_points + stance_curve_points

def plot_trajectory_2(full_trajectory):
    """
    Plots the full trajectory along with its control points.

    Parameters:
    full_trajectory (list of tuples): Points on the full trajectory.
    """
    full_trajectory = np.array(full_trajectory)
    plt.plot(full_trajectory[:, 0], full_trajectory[:, 1], 'b-', label='Full Trajectory')
    plt.legend()
    plt.xlabel('X coordinate WRT hip (m)')
    plt.ylabel('Y coordinate WRT hip (m)')
    plt.title('Full Foot Trajectory Generation')
    plt.show()




if __name__ == '__main__':

    standx = -0.045
    Lspan= 0.025
    deltaL = 0.02
    delta= 0.01
    standy= -0.34
    Yspan= 0.04
    deltaY= 0.01
    

    control_points = [(-0.07, -0.34), 
                      (-0.09, -0.34), 
                      (-0.1, -0.3), (-0.1, -0.3),(-0.1, -0.3),
                      (-0.045, -0.3),(-0.045, -0.3),
                      (-0.045,-0.29),
                      (0,-0.29),(0,-0.29),
                      (-0.01,-0.34),
                      (-0.03,-0.34)]
    
    print("first control points : \n",control_points)
    control_points = generate_control_points(standx, Lspan, deltaL, delta, standy, Yspan, deltaY)
    print("verification : second control points : \n", control_points)
    bezier_curve_points = bezier(control_points)
    stance_curve_points = stance_phase(bezier_curve_points[-1], bezier_curve_points[0])

    plot_trajectory(control_points, bezier_curve_points, stance_curve_points)
    plot_trajectory_2(generate_trajectory(standx, Lspan, deltaL, delta, standy, Yspan, deltaY))

    d = {'FR_0':0, 'FR_1':1, 'FR_2':2,
         'FL_0':3, 'FL_1':4, 'FL_2':5, 
         'RR_0':6, 'RR_1':7, 'RR_2':8, 
         'RL_0':9, 'RL_1':10, 'RL_2':11 }
    

    PosStopF  = math.pow(10,9)
    VelStopF  = 16000.0
    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff
    sin_mid_q = [0, 1.0,-1.7]
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


    trajectory = generate_trajectory(standx, Lspan, deltaL, delta, standy, Yspan, deltaY)
    ## main loop
    while motiontime < sim_time-1:
        time.sleep(0.002)
        motiontime += 1
        
        
        udp.Recv()
        udp.GetRecv(state)

        

        coord = trajectory[motiontime%len(trajectory)]

        if( motiontime >= 0):

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
                new_motion_time = motiontime - 400 
                print(new_motion_time)
                


                x = coord[0]
                y = coord[1]
                z = 0
                
                qDes[0] = z
                qDes[1] = theta_thigh(x,y,z)
                qDes[2] = theta_calf(x,y,z)

                # qDes[1] = sin_mid_q[1] + 1.6*math.sin(new_motion_time/200)
                # qDes[2] = sin_mid_q[2] + 0.8*math.sin(new_motion_time/200 + math.pi/2)


                print(f"θ_hip: {qDes[0]} radians")
                print(f"θ_thigh: {qDes[1]} radians")
                print(f"θ_calf: {qDes[2]} radians")

            

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

# for i in range(len(oscillator.brain)):
    # t = np.arange(0,len(V[i]))*res          #Define the time axis.
# 
    # plt.figure()                         #Plot the results.
    # plt.plot(t,V[i])
    # plt.xlabel('Time [ms]')
    # plt.ylabel('Voltage [mV]');
    # plt.show()
