import os
import sys
from itertools import product


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator


class Controller(Organ): 

    ## use DEFINE value such as SHOULD, KNEE...


    frequencies = [
            0,
            3.003003003003003,
            3.6032217041119123,
            4.504504504504505,
            # 5.9880239520958085,
            6.005384137502588,
            9.00900900900901
        ]
    N_REPEAT = 4




    # value - offset 

    def pass_inputs(self,input):  
        for os in self.oscillators : 
            os.brain[0].inputs[1] = input

    # def simulate(self,k,V):
        # for i in range (len(self.oscillators)) : 
                # self.oscillators[i].simulate(k,V[i])

    def find_combination_index(self, ratio):
        distance = 2
        index = 0
        for i in range(len(self.main_list)):
            new_d = abs(ratio - self.main_list[i][0])
            if new_d<distance:
                index = i
                distance = new_d
        return index,distance 


    def find_combination(self, ratio):
        i, d = self.find_combination_index(ratio)
        return self.main_list[i][1],self.main_list[i][0]


    def build_combinations(self, lower_bound=-2, upper_bound=2):
        new_center = (upper_bound + lower_bound)/2
        amplitude = (upper_bound - lower_bound)/2


        numbers = self.frequencies
        
        # Générer toutes les combinaisons possibles de N_REPEAT nombres (avec répétition)
        comb_of_six_with_repetition = list(product(numbers, repeat=self.N_REPEAT))

        # Ensemble pour stocker les résultats et leurs triplés sans doublon
        results_with_triples = set()

        # Générer toutes les combinaisons de + et - (2^N_REPEAT combinaisons)
        sign_combinations = list(product([1, -1], repeat=self.N_REPEAT))

        # Parcourir chaque combinaison de nombres avec répétition
        for combo in comb_of_six_with_repetition:
            # Pour chaque combinaison de signes, appliquer les signes aux nombres
            for signs in sign_combinations:
                # Calculer la somme pondérée par les signes
                numbers = sum(sign * num for sign, num in zip(signs, combo))

                # Construire le triplé avec les signes appliqués
                operation_triple = tuple(sign * num for sign, num in zip(signs, combo))

                # Ajouter le résultat et le triplé à l'ensemble
                results_with_triples.add((numbers, operation_triple))

        # Convertir l'ensemble en une liste triée des résultats avec leurs triplés
        sorted_results_with_triples = sorted(results_with_triples)

        # Normaliser les résultats selon les bornes spécifiées
        results = [r for r, _ in sorted_results_with_triples]
        
        max_sum_frequency = self.frequencies[-1]*self.N_REPEAT

        normalized_results_with_triples = []

        for value, triple in sorted_results_with_triples:
            # print("value : ", value)
            # Normaliser à [0, 1]
            # if value <0 : print("value ! ",value)
            # print("value : ", value)
            raw_ratio = value / max_sum_frequency
            normalized_ratio = raw_ratio * amplitude
            
            # Échelle à [lower_bound, upper_bound]
            # scaled_value = lower_bound + normalized_value * (upper_bound - lower_bound)
            
            # Centrer autour de `center`
            centered_ratio = normalized_ratio + new_center

            normalized_results_with_triples.append((centered_ratio, triple))

        return normalized_results_with_triples
    

    
    def create_oscillators(self,ratio):

        tuple, true_val = self.find_combination(ratio)

        assert len(tuple) == self.N_REPEAT
        i = 0
        for j in tuple:
            
            if j == 0 : 
                sign = 1
            else :
                sign = j//abs(j)

            current = self.oscillators[i]

            if abs(j) == self.frequencies[0]:
                current.tune_oscillator([0.015,0.015],sign)#0

            if abs(j) == self.frequencies[1]: #3.003003003003003
                current.tune_oscillator([7.5,7.5],sign)

            if abs(j) == self.frequencies[2]:# 3.6032217041119123 
                current.tune_oscillator([7.65,7.65],sign)

            if abs(j) == self.frequencies[3]: # 4.504504504504505
                current.tune_oscillator([7.8,7.8],sign)

            if abs(j) == self.frequencies[4]: #6.024096385542169
                current.tune_oscillator([8.325,8.325],sign)

            if abs(j) == self.frequencies[5]: #9.00900900900901
                current.tune_oscillator([10.65,10.65],sign)

            i+=1
        # self.pass_inputs(1)
        return true_val
            

    def __init__(self, res):
        super().__init__()
        self.name = "Controller"
        self.res = res
        self.oscillators = [Tunable_Oscillator(res = self.res) for i in range (self.N_REPEAT)]
        self.main_list = self.build_combinations()
        self.brain = [neuron for oscillator in self.oscillators for neuron in oscillator.brain]

        print("len :  \n",len(self.brain))