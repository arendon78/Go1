from forces.utils_forces import *   

class Foot_Sensor() : 
    parts= ['FR', 'FL','RR','RL']

    def __init__(self) :
        self.present_frames = {part : [] for part in self.parts}
        self.feet_detected = {part : part + " foot not detected" for part in self.parts} 
        self.old_point = {part : [] for part in self.parts}
        self.new_point = {part : [] for part in self.parts}
    
    def get_foot_detected(self, part) : 
        return self.feet_detected[part]
    
    def reset_detection(self,part): 
        self.feet_detected[part] = part + " foot not detected"

    def detect(self,new_motion_time,force,part) : 
            # self.feet_detected[part] = part +  " foot detected"
            # print("inside detect : ", new_motion_time,force)
            if new_motion_time == 0 : 
                self.new_point[part] = [new_motion_time,force]
            else : 
                self.old_point[part] = self.new_point[part]
                self.new_point[part] = [new_motion_time, force]
                
                self.old_point[part] = self.old_point[part] + [calculate_derivative(self.new_point[part],self.old_point[part])]
                #---you have a delay of 1 point...
                
                self.present_frames[part].append(self.old_point[part])
                if len(self.present_frames[part])%20 == 0 : 
                    local_maxes = monte_carlo_gradient(1,self.present_frames[part])
                    local_mins = monte_carlo_gradient(-1,self.present_frames[part])
                    new_merged_mins_maxes_coordinates = build_merge(local_maxes, local_mins)
                    if part == "FR" : 
                        print('FR : ')
                        # print(self.present_frames[part])
                        bool, p0,p1,p2 = find_a_pattern(new_merged_mins_maxes_coordinates,self.present_frames[part],400,400,4)
                    elif part == "FL" : 
                        print("FL: ")
                        bool, p0,p1,p2 = find_a_pattern(new_merged_mins_maxes_coordinates,self.present_frames[part],700,700,5.5)
                    else : 
                        print( "detecting a step pattern on a limb ith no filter developped")
                    if bool :
                        # print("pattern found !\n\n",p0,p1,p2)#-----------this is typically where we would take action after the recognition of a step.
                        print("pattern found ! at : ", new_motion_time,"for part : ", part)
                        self.feet_detected[part] = part +  " foot detected"
                        self.present_frames[part] = []