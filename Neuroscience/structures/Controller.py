import os
import sys
from itertools import product


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator
from Neuroscience.structures.Frequency_Detector import Frequency_Detector

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

    def simulate(self,k,V):

        for i in range (len(self.oscillators)) : 
                self.oscillators[i].simulate(k,V[i])

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


    #list of doubles :
    # (normalized sum of different possiblefiring rates of  oscillator, 
    # the specific combination to perform it)
    # def build_combinations(self):
    #     numbers = self.frequencies
        
    #     # La liste des nombres

    #     # Générer toutes les combinaisons possibles de 6 nombres (avec répétition)
    #     comb_of_six_with_repetition = list(product(numbers, repeat=self.N_REPEAT))

    #     # Ensemble pour stocker les résultats et leurs triplés sans doublon
    #     results_with_triples = set()

    #     # Générer toutes les combinaisons de + et - (2^6 = 64 combinaisons)
    #     sign_combinations = list(product([1, -1], repeat=self.N_REPEAT))

    #     # Parcourir chaque combinaison de six nombres avec répétition
    #     for combo in comb_of_six_with_repetition:
    #         # Pour chaque combinaison de signes, appliquer les signes aux nombres
    #         for signs in sign_combinations:
    #             # Calculer la somme pondérée par les signes
    #             numbers = sum(sign * num for sign, num in zip(signs, combo))

    #             # Construire le triplé avec les signes appliqués
    #             operation_triple = tuple(sign * num for sign, num in zip(signs, combo))

    #             # Ajouter le résultat et le triplé à l'ensemble
    #             results_with_triples.add((numbers, operation_triple))

    #     # Convertir l'ensemble en une liste triée des résultats avec leurs triplés
    #     sorted_results_with_triples = sorted(results_with_triples)

    #     #normalize
    #     results = []
    #     [results.append(r) for r,_ in results_with_triples ]
    #     m = max(results)
    #     l=list(results_with_triples)
    #     lprime = []

    #     for i in range(len(l)):
    #         lprime.append((l[i][0]/m,l[i][1]))

    #     return lprime


    # def build_combinations(self, amplitude=2):
    #     numbers = self.frequencies
        
    #     # La liste des nombres

    #     # Générer toutes les combinaisons possibles de 4 nombres (avec répétition)
    #     comb_of_six_with_repetition = list(product(numbers, repeat=self.N_REPEAT))

    #     # Ensemble pour stocker les résultats et leurs triplés sans doublon
    #     results_with_triples = set()

    #     # Générer toutes les combinaisons de + et - (2^4 = 16 combinaisons)
    #     sign_combinations = list(product([1, -1], repeat=self.N_REPEAT))

    #     # Parcourir chaque combinaison de six nombres avec répétition
    #     for combo in comb_of_six_with_repetition:
    #         # Pour chaque combinaison de signes, appliquer les signes aux nombres
    #         for signs in sign_combinations:
    #             # Calculer la somme pondérée par les signes
    #             numbers = sum(sign * num for sign, num in zip(signs, combo))

    #             # Construire le triplé avec les signes appliqués
    #             operation_triple = tuple(sign * num for sign, num in zip(signs, combo))

    #             # Ajouter le résultat et le triplé à l'ensemble
    #             results_with_triples.add((numbers, operation_triple))

    #     # Convertir l'ensemble en une liste triée des résultats avec leurs triplés
    #     sorted_results_with_triples = sorted(results_with_triples)

    #     # Normalize using the specified amplitude
    #     results = []
    #     [results.append(r) for r, _ in results_with_triples]
    #     max_result = max(results)
    #     min_result = min(results)
    #     normalized_results_with_triples = []

    #     for value, triple in sorted_results_with_triples:
    #         print("min_result : ",min_result)
    #         normalized_value = amplitude * (value - min_result) / (max_result - min_result) * 2 - amplitude
    #         normalized_results_with_triples.append((normalized_value, triple))

    #     return normalized_results_with_triples


    # def build_combinations(self, amplitude=0.40):
    #     numbers = self.frequencies
        
    #     # La liste des nombres

    #     # Générer toutes les combinaisons possibles de 4 nombres (avec répétition)
    #     comb_of_six_with_repetition = list(product(numbers, repeat=self.N_REPEAT))

    #     # Ensemble pour stocker les résultats et leurs triplés sans doublon
    #     results_with_triples = set()

    #     # Générer toutes les combinaisons de + et - (2^4 = 16 combinaisons)
    #     sign_combinations = list(product([1, -1], repeat=self.N_REPEAT))

    #     # Parcourir chaque combinaison de six nombres avec répétition
    #     for combo in comb_of_six_with_repetition:
    #         # Pour chaque combinaison de signes, appliquer les signes aux nombres
    #         for signs in sign_combinations:
    #             # Calculer la somme pondérée par les signes
    #             numbers = sum(sign * num for sign, num in zip(signs, combo))

    #             # Construire le triplé avec les signes appliqués
    #             operation_triple = tuple(sign * num for sign, num in zip(signs, combo))

    #             # Ajouter le résultat et le triplé à l'ensemble
    #             results_with_triples.add((numbers, operation_triple))

    #     # Convertir l'ensemble en une liste triée des résultats avec leurs triplés
    #     sorted_results_with_triples = sorted(results_with_triples)

    #     # Normalize to [-1, 1]
    #     results = []
    #     [results.append(r) for r, _ in results_with_triples]
    #     max_result = max(results)
    #     min_result = min(results)
    #     range_result = max_result - min_result
    #     normalized_results_with_triples = []

    #     for value, triple in sorted_results_with_triples:
    #         normalized_value = (value - min_result) / range_result * 2 - 1
    #         # Scale to [-amplitude, amplitude]
    #         scaled_value = normalized_value * amplitude
    #         normalized_results_with_triples.append((scaled_value, triple))

    #     return normalized_results_with_triples


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
        self.oscillators = []
        self.set_changed_instance(True)
        tuple, true_val = self.find_combination(ratio)

        assert len(tuple) == self.N_REPEAT
        for j in tuple:
            if j ==0 : 
                sign = 1
            else :
                sign = j//abs(j)
            to_app = Tunable_Oscillator(type = sign, res = self.res)
            if abs(j) == self.frequencies[0]: 
                to_app.tune(2,[0.015,0.015])#0

            if abs(j) == self.frequencies[1]: #3.003003003003003
                to_app.tune(2,[7.5,7.5])

            if abs(j) == self.frequencies[2]:# 3.6032217041119123 
                to_app.tune(2,[7.65,7.65])

            if abs(j) == self.frequencies[3]: # 4.504504504504505
                to_app.tune(2,[7.8,7.8])

            # if abs(j) == self.frequencies[4]: #5.9880239520958085
                # to_app.tune(2,[7.95,7.95])

            if abs(j) == self.frequencies[4]: #6.024096385542169
                to_app.tune(2,[8.325,8.325])

            if abs(j) == self.frequencies[5]: #9.00900900900901
                to_app.tune(2,[10.65,10.65])
            self.oscillators.append(to_app)
        # self.pass_inputs(1)
        return true_val

    def set_changed_instance(self,bool): 
        self.changed_instance = bool

    def get_changed_instance(self): 
        return self.changed_instance

        
            

    def __init__(self, res):
        super().__init__()
        self.res = res
        self.oscillators = []
        self.main_list = self.build_combinations()
        self.set_changed_instance(True)
        # print("main list  : ")
        # [print(self.main_list[i]) for i in range(100)]


