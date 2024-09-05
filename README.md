# Go1
Unitree Go1 Edu Quadruped Development environment


if you got any problems, you can refer to this video (also for network configuration)
https://www.youtube.com/watch?v=o6JtfTM3ArY&

Setup : The robot sould be lying on the ground.



0.1. install the virtual environment 
    0.1.1. install conda
    0.1.2. got to Go1/
    0.1.3  conda create --name go1 python=3.8
    0.1.4  conda activate go1
    0.1.5  pip install -r requirements.txt
    0.1.6  If you got any other problems with some libraries not installed : install them.
    0.1.7  If it tells you that manim is not installed when running the animation module : install it manually using the README.md file in the animation module

if it asks you, [Y/n], type Y

1. Turn on the robot : gentle push and then prolonged push 
2. Wait until the robot turns on and stand up. 
3.Put Go1 into low level programming mode:
L2 + A
L2 + A
L2 + B
L1 + L2 + Start
using the controller
4.Conntect to the wifi network : Unitree-G01...
5.open a new terminal (2)
6. in terminal (2) write 'ssh pi@192.168.12.1'
7. Type password : '123'
8.network configuration : normally you don't need to do it, try withtout and if it doesn't work, you will do it.
Now you are connected to the robot, you can send him instructions
9.attach the robot to the metal frame and lift it up
10.run sample code to make sure everything works fine: 
    10.1. Go to Go1/src/unitree_legged/example_py/old_example/
    10.2. activate conda environment : 'conda activate go1'
    10.3. execute test code : 'python example_position.py'

the 3 joints of the robot front left leg should move smoothly without weird noises.
If it works congratulation, the robot is ready for more advanced commands. 
11.you can execute the script src/unitree_legged/example_py/Bezier/forward_neuron.py after putting the robot down
    make sure that the function called is main_loop and not main_loop_v2


