#!/usr/bin/python
import os 
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)


from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator

sys.path.append('../../lib/python/amd64')
from unitree_legged_sdk.lib.python import robot_interface as sdk



##DEPRECATED--------------------------------------------------------------------------------

def jointLinearInterpolation(initPos, targetPos, rate):

    rate = np.fmin(np.fmax(rate, 0.0), 1.0)
    p = initPos*(1-rate) + targetPos*rate
    return p

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

def bezier(points, num_points=50):
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



def stance_phase(start_point, end_point, num_points=50, delta = 0.007):
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

def generate_trajectory(standx, Lspan, deltaL, delta, standy, Yspan, deltaY, num_points_bezier = 50, num_points_stance = 50):
    points = generate_control_points(standx, Lspan, deltaL, delta, standy, Yspan, deltaY)
    bezier_curve_points = bezier(points,num_points=num_points_bezier)
    stance_curve_points = stance_phase(bezier_curve_points[-1], bezier_curve_points[0],delta=delta,num_points=num_points_stance)

    return bezier_curve_points + stance_curve_points

def unphase(deg, list):
    assert deg>=0 and deg <= 360
    index =int(deg/360*len(list))
    toreturn = list[index:]+list[:index]
    return toreturn


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

def plot_trajectory_3(bezier_points, stance_points):
    bezier_curve = np.array(bezier_points)
    stance_curve = np.array(stance_points)

    plt.scatter(bezier_curve[:, 0], bezier_curve[:, 1], c=np.linspace(0, 1, len(bezier_curve)), cmap='viridis', label='Swing Phase', s=10)
    plt.scatter(stance_curve[:, 0], stance_curve[:, 1], c=np.linspace(0, 1, len(stance_curve)), cmap='plasma', label='Stance Phase', s=10)
    plt.legend(['Start', 'End'])
    plt.xlabel('X coordinate WRT hip (m)')
    plt.ylabel('Y coordinate WRT hip (m)')
    plt.title('Forward Gait Foot Trajectory')
    plt.show()


def plot_joint_angles(full_trajectory):
    full_trajectory = np.array(full_trajectory)
    num_points = len(full_trajectory)
    
    hip_angles = np.zeros(num_points)
    thigh_angles = np.zeros(num_points)
    calf_angles = np.zeros(num_points)
    
    for i in range(num_points):
        x, y = full_trajectory[i]
        hip_angles[i] = theta_hip(0, y)
        thigh_angles[i] = theta_thigh(x, y, 0)
        calf_angles[i] = theta_calf(x, y, 0)
    
    t = np.arange(num_points)
    
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(t, thigh_angles, c=np.linspace(0, 1, num_points), cmap='viridis', label='Thigh Joint Solution', s=10)
    plt.xlabel('Timesteps')
    plt.ylabel('Angle (radians)')
    plt.title('Thigh Joint Solution')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.scatter(t, calf_angles, c=np.linspace(0, 1, num_points), cmap='plasma', label='Calf Joint Solution', s=10)
    plt.xlabel('Timesteps')
    plt.ylabel('Angle (radians)')
    plt.title('Calf Joint Solution')
    plt.legend()
    
    plt.tight_layout()
    plt.show()



if __name__ == '__main__':

    standx = -0.045
    # standx = -0
    Lspan= 0.025
    # Lspan = 0.05
    deltaL = 0.02
    # deltaL = 0.04
    delta= 0.02
    standy= -0.35
    Yspan= 0.04
    # Yspan= 0.06
    deltaY= 0.01
    #works with 100, we'll just try and simulate with 10
    # NUM_POINST_BEZIER = 100
    # NUM_POINTS_STANCE = 100

    # NUM_POINST_BEZIER = 50
    # NUM_POINTS_STANCE = 50


    NUM_POINST_BEZIER = 5
    NUM_POINTS_STANCE = 5

    trajectory = generate_trajectory(standx, Lspan, deltaL, delta, standy, Yspan, deltaY,num_points_bezier=NUM_POINST_BEZIER, num_points_stance= NUM_POINTS_STANCE)
    

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
    plot_trajectory_2(generate_trajectory(standx, Lspan, deltaL, delta, standy, Yspan, deltaY))   
    plot_trajectory_3(bezier_curve_points,stance_curve_points)
    plot_joint_angles(trajectory)


    d = {'FR_0':0, 'FR_1':1, 'FR_2':2,
         'FL_0':3, 'FL_1':4, 'FL_2':5, 
         'RR_0':6, 'RR_1':7, 'RR_2':8, 
         'RL_0':9, 'RL_1':10, 'RL_2':11 }
    

    PosStopF  = math.pow(10,9)
    VelStopF  = 16000.0
    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff
    # stand_up_1 = {'FR' : [0, 0.7,-1.75] , 'FL' : [0, 0.7,-1.75 ] ,'RR' : [0, 1,-0.8], 'RL' : [0, 1,-0.8] }
    #has a built-in asymetry or default...
    bias_default = 0
    # stand_up_1 = {'FR' : [0, 0.75,-1.75] , 'FL' : [0, 0.75,-1.75 ] ,'RR' : [0, 1,-0.9], 'RL' : [0, 1,-0.9] }
    # stand_up_2 = {'FR' : [0, 0.75,-1.20] , 'FL' : [0, 0.75,-1.20 ] ,'RR' : [0, 1.05,-0.9], 'RL' : [0, 1.05,-0.9] }
    # stand_up_3 = {'FR' : [0, 0.75,-1.20] , 'FL' : [0, 0.75,-1.20 ] ,'RR' : [0, 1.05,-1.2], 'RL' : [0, 1.05,-1.2] }
    # print('trajectory[0] : ',trajectory[0])

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
    sim_time = 10000
    V = [np.zeros([sim_time,1]), np.zeros([sim_time,1]), np.zeros([sim_time,1])]
    inputs = np.zeros([sim_time,1])            #Initialize V.
    inputs[1] = [1]

    offset_cycle_FR = 0
    offset_cycle_FL = 1
    offset_cycle_RR = 1
    offset_cycle_RL = 0
    TOTAL_OFFSET = 1

    FR_trajectory = unphase(0,trajectory)
    FL_trajectory = unphase(0,trajectory)
    RR_trajectory = unphase(0,trajectory)
    RL_trajectory = unphase(0,trajectory)

    trajectories = {'FR': [trajectory[0]]* len(trajectory) * offset_cycle_FR +  FR_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_FR ) ,
                    'FL': [trajectory[0]]* len(trajectory) * offset_cycle_FL +  FL_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_FL ),
                    'RR': [trajectory[0]]* len(trajectory) * offset_cycle_RR +  RR_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_RR ),
                    'RL': [trajectory[0]]* len(trajectory) * offset_cycle_RL +  RL_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_RL )
                    }
    
 
    print("\n\n -------- trajectories ---------- \n\n")

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





    ## main loop
    while motiontime < sim_time-1:
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


        STAND_UP_TIME = 1000
        WALKING_TIME = 2000
        INIT_TIME = 10


        if( motiontime >= 0):
            print(motiontime)

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
                # Kp = [75, 75, 75]
                Kp = [60, 60, 60]
                Kd = [5,5, 5]
                
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


#walking phase ---------------------------------------------------------------------

            if( motiontime >= STAND_UP_TIME + INIT_TIME and motiontime<STAND_UP_TIME + WALKING_TIME + INIT_TIME):
                new_motion_time = motiontime - (STAND_UP_TIME + INIT_TIME)
                print(new_motion_time)
                # 
# 
                for part in parts :
# 
                    x = coords[part][0]
                    y = coords[part][1]
                    z = 0
# 
                    # for number in ['_0','_1','_2']: 
                    qDes[part][0] = z
                    qDes[part][1] = theta_thigh(x,y,z)
                    qDes[part][2] = theta_calf(x,y,z)
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
                # print(d[part + '_0'])
                # if ( part == "FL"):# restrains to only one leg
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





# https://chatgpt.com/c/1c470053-e91e-4b92-9305-18bbef479ede
# import numpy as np

# # Exemple de tableau NumPy
# tableau_numpy = np.array([1, 2, 3, 4, 5])

# # Sauvegarde du tableau NumPy
# np.save('tableau.npy', tableau_numpy)

# # Chargement du tableau NumPy
# tableau_numpy_charge = np.load('tableau.npy')

# print(tableau_numpy_charge)

