import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Frequency_Detector import Frequency_Detector

class Router: 
    def __init__(self, f_detector):
        self.f_detector = f_detector

    def route(self): 
        #route to action the robot should do 