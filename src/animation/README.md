how to install manim manually : 

sudo apt-get update
sudo apt-get install libcairo2-dev pkg-config python3-dev
sudo apt-get install libpango1.0-dev
 



you should also install ffmpeg if you don't have it. 

'sudo apt install ffmpeg'

if it doesn't work then try

'sudo apt install build-essential libcairo2-dev pkg-config python3-dev'

and try again 

'pip install manim'

How to animate the neural network  of the robot : 
- if it doesn t exist, create a file nammed 'datas' in the /animatiom/ directory
- Activate your virtual environment
- *Activate the neuron simulation* by changing the value of the variable 'compute_simulation' to True in the file 'forward_neuron' in the directory unitree_legged_sdk/example_py/Bezier
- *Run the simulation* by running the main file : 'python forward_neuron.py'. It is located in 'unitree_legged_sdk/example_py/Bezier'
- Once the neural netwrok is simulated, the file is located in '/unitree_legged_sdk/example_py/Bezier/data/neuron_activity.json'
- Begin the animation of the neural network : go in 'animation/' and type 'manim -pql display_neural_network.py'

- If you want a better visual quality, type 'manim -p display_neural_network.py'

- Once the computation is finished, it should open the video automatically. If not, the mp4 file is also available in the animation/media/video/ directory.

- If you want to do another animation, you don't need to do the simulation of the neural network again, as it is saved in a file.
- Simulating the neural network again will automatically replace the previous file of the neural activity


How to animate any neural network :

- Go to Neuroscience/tests/simulate_any/
- in the /sim/ file, create the file for your neural network (your neural network should be a class that inherits from Organ).
    - make sure that your class has a name attribute
- In this file, define a function called instance_and_input(sim_time) that returns the instance of your network and the inputs you want to give him during the simulation
- in the simulate_any.py file, import the module that you just created (read the comments)
- run the file : 'python simulate_any.py'

- Go to /animation/ module 
- change the "name" value to the name of your instance (the one you defined in its definition)
- run the file 'python animate_any.py'
 

## BE CAREFUL : If you do low quality (-pql option) make sure that the interval between each neuron in the activation function is the good one.