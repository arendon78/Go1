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

    range0 = 1.8
    offset0 = 0.5

    range1=4.7
    offset1 = 0.7

    range2=2.3
    offset3= 3.0


    frequencies = [
            0,
            30.030030030030026,
            36.101083032490976,
            45.045045045045036,
            59.880239520958085,
            60.24096385542168,
            90.09009009009007
        ]
    N_REPEAT = 5




    # value - offset 

    def find_combination_index(self, ratio):
        distance = 1
        index = 0
        for i in range(len(self.main_list)):
            new_d = abs(ratio - self.main_list[i][0])
            if new_d<distance:
                index = i
                distance = new_d
        print(index)
        return index 


    def find_combination(self, ratio):
        return self.main_list[self.find_combination_index(ratio)][1]


    #list of doubles :
    # (normalized sum of different possiblefiring rates of  oscillator, 
    # the specific combination to perform it)
    def build_combinations(self):
        numbers = self.frequencies
        
        # La liste des nombres

        # Générer toutes les combinaisons possibles de 6 nombres (avec répétition)
        comb_of_six_with_repetition = list(product(numbers, repeat=self.N_REPEAT))

        # Ensemble pour stocker les résultats et leurs triplés sans doublon
        results_with_triples = set()

        # Générer toutes les combinaisons de + et - (2^6 = 64 combinaisons)
        sign_combinations = list(product([1, -1], repeat=self.N_REPEAT))

        # Parcourir chaque combinaison de six nombres avec répétition
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

        # Optionnel: Afficher tous les nombres possibles avec leurs triplés correspondants
        # for result, triple in sorted_results_with_triples:
            # print(f"{result} = {triple}")

        # Extraire uniquement les résultats triés
        # sorted_results_only = sorted(result for result, _ in sorted_results_with_triples)

        # Retourner la liste des résultats triés
        # for j in sorted_results_only:s
            # print(j)

        #normalize
        results = []
        [results.append(r) for r,_ in results_with_triples ]
        m = max(results)
        l=list(results_with_triples)
        lprime = []

        for i in range(len(l)):
            lprime.append((l[i][0]/m,l[i][1]))

        return lprime
    
    def create_oscillators(self,ratio):
        tuple = self.find_combination(ratio)
        print("tuple in create_oscillators",tuple)
        print("verification : ", sum(tuple)/(90.09009009009007*self.N_REPEAT))
        assert len(tuple) == self.N_REPEAT
        for j in tuple:
            if j ==0 : 
                sign = 1
            else :
                sign = j//abs(j)
            to_app = Tunable_Oscillator(type = sign, res = self.res)
            if abs(j) == self.frequencies[0]: 
                to_app.tune(2,[0.015,0.015])

            if abs(j) == self.frequencies[1]: 
                to_app.tune(2,[7.5,7.5])

            if abs(j) == self.frequencies[2]: 
                to_app.tune(2,[7.53,7.53])

            if abs(j) == self.frequencies[3]: 
                to_app.tune(2,[7.695,7.695])

            if abs(j) == self.frequencies[4]: 
                to_app.tune(2,[7.935,7.935])

            if abs(j) == self.frequencies[5]: 
                to_app.tune(2,[8.325,8.325])

            if abs(j) == self.frequencies[6]: 
                to_app.tune(2,[10.53,10.53])
            self.oscillators.append(to_app)
        
    def activate(self):
        for i in range(self.N_REPEAT):
            self.oscillators[i].brain[0].inputs[1] = 1
    
    # def simulate(self,k,V):
    #     if len(V) != self.N_REPEAT:
    #         print("problem with V size !")
    #     for i in range (self.N_REPEAT) : 
    #         self.oscillators[i].simulate(k, V[i])
        
            

    def __init__(self, res):
        super().__init__()
        self.res = res
        self.oscillators = []
        self.main_list = self.build_combinations()


