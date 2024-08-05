#!/usr/bin/python
import os 
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt

from utils import *


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)


def plot_everything(neurons_coords, command_coords, frequency_parts, command, inside_oscillator):
    plot_trajectory_single(neurons_coords['FR'],(0,1), 'Theta hip (radian)', 'Theta thigh (radian)')
    plot_trajectory_single(command_coords['FR'],(0,1), 'Theta hip (radian)', 'Theta calf (radian)')

    plot_trajectory_single(neurons_coords['FR'],(1,2), 'Theta thigh (radian)', 'Theta calf (radian)')
    plot_trajectory_single(command_coords['FR'],(1,2), 'Theta thigh (radian)', 'Theta calf (radian)')

    plot_trajectory_single(neurons_coords['FR'],(2,0), 'Theta calf (radian)', 'Theta hip (radian)')
    plot_trajectory_single(command_coords['FR'],(2,0), 'Theta calf (radian)', 'Theta hip (radian)')

    freq0 = np.array(frequency_parts['FR'][0])
    freq1 = np.array(frequency_parts['FR'][1])
    freq2 = np.array(frequency_parts['FR'][2])

    oscillator0_data = np.array(inside_oscillator['FR'][0])
    oscillator1_data = np.array(inside_oscillator['FR'][1])
    oscillator2_data = np.array(inside_oscillator['FR'][2])

    freq_command0 = np.array(command['FR'][0])
    freq_command1 = np.array(command['FR'][1])
    freq_command2 = np.array(command['FR'][2])

    xfreq0 =np.arange(len(freq0))
    xfreq1 = np.arange(len(freq1)) # x1
    xfreq2 = np.arange(len(freq2)) # x2
    xfreq_command0 = np.arange(len(freq_command0))
    xfreq_command1 = np.arange(len(freq_command1)) # x3
    xfreq_command2 = np.arange(len(freq_command2)) # x4
    xoscillator0_data = np.arange(len(oscillator0_data))
    xoscillator1_data = np.arange(len(oscillator1_data)) # x5
    xoscillator2_data = np.arange(len(oscillator2_data)) # x6


    # Créer une figure avec 2 sous-graphiques (2 lignes, 1 colonne)
    fig1, (ax0,ax1, ax2) = plt.subplots(3, 1, figsize=(12, 6))

    ax0.plot(xfreq0, freq0, color="blue", label="Freq 0")
    ax0.plot(xfreq_command0, freq_command0, color="green", label="Command 0")
    ax0.plot(xoscillator0_data, oscillator0_data, color="red", label="Oscillator 0")
    ax0.set_ylabel("Position and Frequency on hip")
    ax0.legend()

    # Tracer les données dans le premier sous-graphe (ax1)
    ax1.plot(xfreq1, freq1, color="blue", label="Freq 1")
    ax1.plot(xfreq_command1, freq_command1, color="green", label="Command 1")
    ax1.plot(xoscillator1_data, oscillator1_data, color="red", label="Oscillator 1")
    ax1.set_ylabel("Position and Frequency on tigh")
    ax1.legend()

    # Tracer les données dans le deuxième sous-graphe (ax2)
    ax2.plot(xfreq2, freq2, color="blue", label="Freq 2")
    ax2.plot(xfreq_command2, freq_command2, color="green", label="Command 2")
    ax2.plot(xoscillator2_data, oscillator2_data, color="red", label="Oscillator 2")
    ax2.set_ylabel("Position and Frequency on calf")
    ax2.legend()

    plt.tight_layout()
    plt.show()