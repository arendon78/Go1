from forces.utils_forces import *

class Foot_Sensor:
    """
    A class to detect foot contact using sensor data and pattern recognition.

    The `Foot_Sensor` class tracks the movement and force data of a robot's foot over time to detect when 
    the foot makes contact with the ground. It utilizes a simple gradient-based pattern recognition to 
    identify specific footfall patterns.

    Attributes
    ----------
    present_frames : dict of list
        A dictionary storing the history of force data points for each foot.
    
    feet_detected : dict of str
        A dictionary indicating whether a foot has been detected as making contact with the ground.
        Initialized with "foot not detected" for each part.
    
    old_point : dict of list
        A dictionary storing the previous force data point for each foot.
    
    new_point : dict of list
        A dictionary storing the current force data point for each foot.
    """

    parts = ['FR', 'FL', 'RR', 'RL']
    """
    List of parts (feet) being monitored, including 'FR' (Front Right), 'FL' (Front Left),
    'RR' (Rear Right), and 'RL' (Rear Left).
    """

    def __init__(self):
        """
        Initializes the Foot_Sensor with default values.

        The constructor sets up empty lists for tracking the force data history (`present_frames`),
        initializes detection statuses (`feet_detected`), and sets up placeholders for old and new
        force data points (`old_point`, `new_point`).
        """
        self.present_frames = {part: [] for part in self.parts}
        self.feet_detected = {part: part + " foot not detected" for part in self.parts}
        self.old_point = {part: [] for part in self.parts}
        self.new_point = {part: [] for part in self.parts}
    
    def get_foot_detected(self, part):
        """
        Returns the detection status of the specified foot part.

        Parameters
        ----------
        part : str
            The part (foot) for which to get the detection status.

        Returns
        -------
        str
            The detection status of the specified foot.
        """
        return self.feet_detected[part]
    
    def reset_detection(self, part):
        """
        Resets the detection status of the specified foot part to "foot not detected".

        Parameters
        ----------
        part : str
            The part (foot) for which to reset the detection status.
        """
        self.feet_detected[part] = part + " foot not detected"

    def detect(self, new_motion_time, force, part):
        """
        Processes the force data for the specified foot part, updating the detection status based on pattern recognition.

        This method tracks the force data over time for each foot and applies a gradient-based pattern recognition 
        algorithm to detect when a foot makes contact with the ground. If a footfall pattern is detected, the foot's 
        detection status is updated.

        Parameters
        ----------
        new_motion_time : float
            The current time point in the motion sequence.
        
        force : float
            The force detected at the specified time point.
        
        part : str
            The part (foot) for which the detection is being performed.
        """
        if new_motion_time == 0:
            self.new_point[part] = [new_motion_time, force]
        else:
            self.old_point[part] = self.new_point[part]
            self.new_point[part] = [new_motion_time, force]
            
            self.old_point[part] += [calculate_derivative(self.new_point[part], self.old_point[part])]
            self.present_frames[part].append(self.old_point[part])
            
            if len(self.present_frames[part]) % 20 == 0:
                local_maxes = monte_carlo_gradient(1, self.present_frames[part])
                local_mins = monte_carlo_gradient(-1, self.present_frames[part])
                new_merged_mins_maxes_coordinates = build_merge(local_maxes, local_mins)
                
                if part == "FR":
                    print('FR:')
                    detected, p0, p1, p2 = find_a_pattern(new_merged_mins_maxes_coordinates, self.present_frames[part], 400, 400, 4)
                elif part == "FL":
                    print('FL:')
                    detected, p0, p1, p2 = find_a_pattern(new_merged_mins_maxes_coordinates, self.present_frames[part], 700, 700, 5.5)
                else:
                    print("Detecting a step pattern on a limb with no filter developed")
                
                if detected:
                    print(f"Pattern found at: {new_motion_time} for part: {part}")
                    self.feet_detected[part] = part + " foot detected"
                    self.present_frames[part] = []
