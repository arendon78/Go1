from utils import *

parts = ["FR","FL","RR","RL"]
STAND_UP_TIME = 1000
INIT_TIME = 10

def stand_up_procedure(motiontime,qInit,state,qDes,d,stand_up_1,rate_count,Kp,Kd) :
    """
    Handles the procedure for the robot to stand up, interpolating joint angles from initial to desired positions.

    Parameters
    ----------
    motiontime : int
        The current time step in the motion sequence.
    
    qInit : dict
        A dictionary containing the initial joint angles for each part (limb).
    
    state : object
        The current state of the robot, including motor states.
    
    qDes : dict
        A dictionary containing the desired joint angles for each part.
    
    d : dict
        A dictionary mapping joint names to their corresponding indices in the robot's state data.
    
    stand_up_1 : dict
        A dictionary containing the target joint angles for each part when the robot is fully standing.
    
    rate_count : int
        A counter used to calculate the interpolation rate.
    
    Kp : list
        Proportional gain values for the robot's joint controllers.
    
    Kd : list
        Derivative gain values for the robot's joint controllers.

    Returns
    -------
    tuple
        Updated values of motiontime, qInit, state, qDes, d, stand_up_1, rate_count, Kp, and Kd.
    """ 
    if( motiontime >= 0):

        if( motiontime >= 0 and motiontime < 10):
            #all this should be encapsualted---------------
            # print("initialise qInit")
            for part in parts : 
                qInit[part][0] = state.motorState[d[part + '_0']].q
                qInit[part][1] = state.motorState[d[part + '_1']].q
                qInit[part][2] = state.motorState[d[part + '_2']].q
#----------------------------------------------------
        if( motiontime >= 10 and motiontime < STAND_UP_TIME +INIT_TIME):
            rate_count += 1
            rate = rate_count/(STAND_UP_TIME//2 - 100)                     # needs count to 500
            Kp = [75, 75, 75]
            Kd = [3, 3, 3]
            # Kd = [5, 5, 5]
            
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
            #until here ---------------------------
    return motiontime,qInit,state,qDes,d,stand_up_1,rate_count,Kp,Kd