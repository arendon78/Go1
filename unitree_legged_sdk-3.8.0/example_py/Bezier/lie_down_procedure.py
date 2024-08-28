
from utils import * 


parts = ["FR","FL","RR","RL"]

STAND_UP_TIME = 1000
INIT_TIME = 10

def lie_down_procedure(new_motion_time,state,qInit,qDes,d,rate_count): 
            
#-------------------------------------------------------------------------
    if (new_motion_time >= 0 and new_motion_time < INIT_TIME):
        for part in parts : 
            qInit[part][0] = state.motorState[d[part + '_0']].q
            qInit[part][1] = state.motorState[d[part + '_1']].q
            qInit[part][2] = state.motorState[d[part + '_2']].q
    if (new_motion_time >=INIT_TIME):
        rate_count += 1
        rate = rate_count/STAND_UP_TIME            # needs count to 200
        sign = 1
        for part in parts : 
            qDes[part][0] = jointLinearInterpolation(qInit[part][0], sign* -0.3161579668521881, rate)
            qDes[part][1] = jointLinearInterpolation(qInit[part][1], 1.208921194076538, rate)
            qDes[part][2] = jointLinearInterpolation(qInit[part][2], -2.7958271503448486, rate)
            sign = sign * -1
    # until here-----------------------------------
    return qDes