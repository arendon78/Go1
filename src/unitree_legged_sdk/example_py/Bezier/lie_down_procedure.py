from utils import * 

parts = ["FR","FL","RR","RL"]

STAND_UP_TIME = 1000
INIT_TIME = 10

def lie_down_procedure(new_motion_time, state, qInit, qDes, d, rate_count): 
    """
    Executes the lie-down procedure for the robot by interpolating motor joint angles 
    from their initial positions to the desired lying down positions.

    Parameters
    ----------
    new_motion_time : int
        The current time step of the motion sequence.
    
    state : object
        The current state of the robot, including motor states.
    
    qInit : dict
        A dictionary storing the initial joint angles for each limb.
    
    qDes : dict
        A dictionary where the desired joint angles for each limb will be stored.
    
    d : dict
        A dictionary mapping each limb's joint to its corresponding index in the state.
    
    rate_count : int
        A counter used to determine the rate of interpolation.

    Returns
    -------
    dict
        The updated `qDes` dictionary containing the interpolated joint angles for the lie-down procedure.
    """
    
    # Capture initial joint positions during the initialization phase
    if (new_motion_time >= 0 and new_motion_time < INIT_TIME):
        for part in parts: 
            qInit[part][0] = state.motorState[d[part + '_0']].q
            qInit[part][1] = state.motorState[d[part + '_1']].q
            qInit[part][2] = state.motorState[d[part + '_2']].q
    
    # Interpolate joint positions towards the desired lying down positions
    if (new_motion_time >= INIT_TIME):
        rate_count += 1
        rate = rate_count / STAND_UP_TIME  # Progress rate towards the desired position
        sign = 1
        for part in parts: 
            qDes[part][0] = jointLinearInterpolation(qInit[part][0], sign * -0.3161579668521881, rate)
            qDes[part][1] = jointLinearInterpolation(qInit[part][1], 1.208921194076538, rate)
            qDes[part][2] = jointLinearInterpolation(qInit[part][2], -2.7958271503448486, rate)
            sign = sign * -1  # Alternate sign for opposite limbs
    
    return qDes
