import numpy as np
import matplotlib.pyplot as plt

import os 
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Flip_FLop_T import Flip_Flop_T
from Neuroscience.structures.Gate_NAND import Gate_NAND
from Neuroscience.structures.Counter_4_bits import Counter_4_bits
from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator


res = 0.1

Control = Controller( res )
Flip_Flo = Flip_Flop_T( res )
Gate_N = Gate_NAND( res = res )
Counter_4_b = Counter_4_bits( res )
Tunable_Oscilla = Tunable_Oscillator( res= res )

list = [
Control,
Flip_Flo,
Gate_N,
Counter_4_b,
Tunable_Oscilla,
]

list_name = [
"Controller",
"Flip_Flop",
"Gate_NAND",
"Counter_4_bits",
"Tunable_Oscillator",
]


for el,name in zip(list,list_name) : 
    el.update_adjacency_matrix()
    el.print_network(name)

# Gate_N.update_adjacency_matrix()
# Gate_N.print_network("Gate_NAND")

# Gate_N.print_network("Gate_NAND")
# Gate_N.print_network("Gate_NAND")
# Gate_N.print_network("Gate_NAND")
# Gate_N.print_network("Gate_NAND")
# Gate_N.print_network("Gate_NAND")
# Gate_N.print_network("Gate_NAND")
# Gate_N.print_network("Gate_NAND")
# Gate_N.print_network("Gate_NAND")
# Gate_N.print_network("Gate_NAND")
# Gate_N.print_network("Gate_NAND")


